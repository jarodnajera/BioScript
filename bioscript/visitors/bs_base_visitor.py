import colorlog

from grammar.parsers.python.BSParser import BSParser
from grammar.parsers.python.BSParserVisitor import BSParserVisitor
from shared.enums.bs_properties import BSTemperature
from shared.enums.bs_properties import BSTime
from shared.enums.bs_properties import BSVolume
from shared.helpers import *


class BSBaseVisitor(BSParserVisitor):

    def __init__(self, symbol_table):
        super().__init__()
        self.log = colorlog.getLogger(self.__class__.__name__)
        self.config = Config.getInstance(None)
        # The identifier to use.
        self.identifier = get_identifier(self.config.identify)
        # The combiner to use.
        self.combiner = get_combiner(self.config.combine)
        self.symbol_table = symbol_table
        self.scope_stack = list()
        self.keywords = ("alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit",
                         "atomic_noexcept", "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char",
                         "char16_t", "char32_t", "class", "compl", "concept", "const", "constexpr", "const_cast",
                         "continue", "co_await", "co_return", "co_yield", "decltype", "default", "delete", "do",
                         "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false", "float",
                         "for", "friend", "goto", "if", "import", "inline", "int", "long", "module", "mutable",
                         "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq",
                         "private", "protected", "public", "reflexpr", "register", "reinterpret_cast", "requires",
                         "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast", "struct",
                         "switch", "synchronized", "template", "this", "thread_local", "throw", "true", "try",
                         "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual", "void", "volatile",
                         "wchar_t", "while", "xor", "xor_eq")

    def visitVolumeIdentifier(self, ctx: BSParser.VolumeIdentifierContext):
        quantity = 10.0
        units = BSVolume.MICROLITRE
        name = ctx.IDENTIFIER().__str__()
        if ctx.VOLUME_NUMBER():
            x = self.split_number_from_unit(ctx.VOLUME_NUMBER().__str__())
            units = BSVolume.get_from_string(x['units'])
            quantity = units.normalize(x['quantity'])
        return {'quantity': quantity, 'units': units,
                'variable': self.symbol_table.get_variable(name, self.scope_stack[-1])}

    def visitTimeIdentifier(self, ctx: BSParser.TimeIdentifierContext):
        x = self.split_number_from_unit(ctx.TIME_NUMBER().__str__())
        units = BSTime.get_from_string(x['units'])
        quantity = units.normalize(x['quantity'])
        return {'quantity': quantity, 'units': units}

    def visitTemperatureIdentifier(self, ctx: BSParser.TemperatureIdentifierContext):
        x = self.split_number_from_unit(ctx.TEMP_NUMBER().__str__())
        units = BSTemperature.get_from_string(x['units'])
        quantity = units.normalize(x['quantity'])
        return {'quantity': quantity, 'units': units}

    def check_identifier(self, name):
        if name in self.keywords:
            return "{}{}".format(name, name)
        else:
            return name

    def split_number_from_unit(self, text):
        temp_float = ""
        temp_unit = ""
        for x in text[0:]:
            if str.isdigit(x):
                temp_float += x
            elif x == ".":
                temp_float += x
            elif x == ",":
                continue
            else:
                temp_unit += x
        return {'quantity': float(temp_float), 'units': temp_unit}
