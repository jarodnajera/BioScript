import chemicals.identifier as identifier
from compiler.data_structures.variable import *
from compiler.semantics.bs_base_visitor import BSBaseVisitor
from grammar.parsers.python.BSParser import BSParser


class GlobalVariableVisitor(BSBaseVisitor):

    def __init__(self, symbol_table, identifier: identifier.Identifier):
        super().__init__(symbol_table, "Global Visitor")
        self.identifier = identifier

    def visitProgram(self, ctx: BSParser.ProgramContext):
        self.visitModuleDeclaration(ctx.moduleDeclaration())
        self.visitManifestDeclaration(ctx.manifestDeclaration())
        self.visitStationaryDeclaration(ctx.stationaryDeclaration())

    def visitModuleDeclaration(self, ctx: BSParser.ModuleDeclarationContext):
        types = {ChemTypes.MODULE}
        for name in ctx.IDENTIFIER():
            var = self.identifier.identify(name.__str__(), types=types, scope=self.global_scope)
            variable = Chemical(var['name'], var['types'], var['scope'])
            variable.is_global = True
            self.symbol_table.add_global(variable)

    def visitManifestDeclaration(self, ctx: BSParser.ManifestDeclarationContext):
        types = {ChemTypes.MAT}
        for name in ctx.IDENTIFIER():
            var = self.identifier.identify(name.__str__(), types=types, scope=self.global_scope)
            variable = Chemical(var['name'], var['types'], var['scope'])
            variable.is_global = True
            self.symbol_table.add_global(variable)

    def visitStationaryDeclaration(self, ctx: BSParser.StationaryDeclarationContext):
        types = {ChemTypes.MAT}
        for name in ctx.IDENTIFIER():
            var = self.identifier.identify(name.__str__(), types=types, scope=self.global_scope)
            variable = Chemical(var['name'], var['types'], var['scope'])
            variable.is_stationary = True
            variable.is_global = True
            self.symbol_table.add_global(variable)