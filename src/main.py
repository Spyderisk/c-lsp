import logging
import datetime
import argparse

from lsprotocol import types
from pygls.lsp.server import LanguageServer
from pygls.workspace import TextDocument
import tree_sitter_c as tsc
from tree_sitter import Language, Parser, Tree, Node

C_LANGUAGE = Language(tsc.language())
parser = Parser(C_LANGUAGE)

trees: dict[str, Tree] = {}


class CLS(LanguageServer):
    """Language server demonstrating "push-model" diagnostics."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diagnostics = {}

    def parse(self, document: TextDocument):
        logging.info(f"Parsing document: {document.filename}")

        src = bytes(document.source, "utf-8")
        old_tree = trees.get(document.uri)

        # TODO: Figure out how to reuse a tree
        # if old_tree:
        # trees[document.uri] = parser.parse(src, old_tree)
        # else:
        trees[document.uri] = parser.parse(src)

        tree = trees[document.uri]
        root = tree.root_node

        diagnostics = []

        def traverse(node: Node):
            if node.type == "ERROR":
                sp = node.start_point
                ep = node.end_point
                logging.error(f"Error node: {node}, sp:{sp}, ep:{ep}")

                diagnostics.append(types.Diagnostic(
                    message="Failed to parse",
                    severity=types.DiagnosticSeverity.Error,
                    range=types.Range(
                        types.Position(sp.row, sp.column),
                        types.Position(ep.row, ep.column),
                    )
                ))
            else:
                for child in node.children:
                    traverse(child)

        logging.debug(f"Tree:\n{tree.root_node}")

        traverse(root)

        self.diagnostics[document.uri] = (document.version, diagnostics)
        # diagnostics = []

        # for idx, line in enumerate(document.lines):
        #     match = ADDITION.match(line)
        #     if match is not None:
        #         left = int(match.group(1))
        #         right = int(match.group(2))

        #         expected_answer = left + right
        #         actual_answer = match.group(3)

        #         if actual_answer is not None and expected_answer == int(actual_answer):
        #             continue

        #         if actual_answer is None:
        #             message = "Missing answer"
        #             severity = types.DiagnosticSeverity.Warning
        #         else:
        #             message = f"Incorrect answer: {actual_answer}"
        #             severity = types.DiagnosticSeverity.Error

        #         diagnostics.append(
        #             types.Diagnostic(
        #                 message=message,
        #                 severity=severity,
        #                 range=types.Range(
        #                     start=types.Position(line=idx, character=0),
        #                     end=types.Position(line=idx, character=len(line) - 1),
        #                 ),
        #             )
        #         )

        # self.diagnostics[document.uri] = (document.version, diagnostics)


server = CLS('c-lsp', 'v0.1')


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: CLS, params: types.DidOpenTextDocumentParams):
    """Parse each document when it is opened"""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    ls.parse(doc)

    for uri, (version, diagnostics) in ls.diagnostics.items():
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=uri,
                version=version,
                diagnostics=diagnostics,
            )
        )


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: CLS, params: types.DidOpenTextDocumentParams):
    """Parse each document when it is changed"""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    ls.parse(doc)

    for uri, (version, diagnostics) in ls.diagnostics.items():
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=uri,
                version=version,
                diagnostics=diagnostics,
            )
        )


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tcp",
        # "127.0.0.1:5007", # Breaks the argument parsing as tcp is always set
        help="Sets the LSP to communicate over TCP with ip:port"
    )

    args = parser.parse_args()

    logging.basicConfig(filename='lsp.log', filemode='w', level=logging.DEBUG)
    logging.info(f"Started Server {datetime.datetime.now()}")

    if args.tcp:
        ip, port = args.tcp.split(':')
        print(f"Starting IO on TCP {ip}:{port}")
        server.start_tcp(ip, int(port))
    else:
        print(f"Starting IO on STDIO")
        server.start_io()


if __name__ == "__main__":
    run()
