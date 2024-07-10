# _plugins/gdb_lexer.rb
require 'rouge'

module Rouge
  module Lexers
    class GDB < RegexLexer
      title "GDB"
      desc "GDB session output"
      tag 'gdb'
      aliases 'gdb'
      filenames '*.gdb'

      def self.keywords
        @keywords ||= Set.new %w(
          info disassemble
        )
      end

      def self.keywords_type
        @keywords_type ||= Set.new %w(
          add jmp
          )
      end

      state :root do
        # Rule for lines beginning with (gdb) followed by any command
        rule /^\(gdb\).*/, Generic::Prompt
        rule /\s+/m, Text::Whitespace
        rule /0x[0-9a-z]+/, Num::Hex
        rule /[\(,\)]/, Punctuation
        rule /\%[a-z0-9]{2,3}/, Name::Variable
        rule /\d+/, Num::Integer
        rule /\S+/, Text
      end
    end
  end
end

# Sample input to test the lexer
# sample_input = <<~EOF
# (gdb) list
# 0x00401560 <main+0>:    55                      push   %rbp
# 0x00401561 <main+1>:    48 89 e5                mov    %rsp,%rbp
# (gdb) disassemble $pc-20,$pc+20
# Dump of assembler code from 0x7fbaa4653c1c to 0x7fbaa4653c44:
# 0x00007fbaa4653c1c:  add    %al,(%rax)
#    0x00007fbaa4653c1e:  jmp    0x7fbaa4653a51
#    0x00007fbaa4653c23:  nopl   0x0(%rax,%rax,1)
#    0x00007fbaa4653c28:  mov    0x98(%r12),%rax
# => 0x00007fbaa4653c30:  cmpb   $0x48,(%rax)
#    0x00007fbaa4653c33:  jne    0x7fbaa4653b90
#    0x00007fbaa4653c39:  movabs $0x50f0000000fc0c7,%rdx
#    0x00007fbaa4653c43:  cmp    %rdx,0x1(%rax)
# End of assembler dump.
# (gdb) bt
# #0  0x00007fbaa4653c30 in ?? ()
# #1  0x0000000000000000 in ?? ()
# EOF
#
# # Instantiate the lexer and formatter
# lexer = Rouge::Lexers::GDB.new
# formatter = Rouge::Formatters::Terminal256.new
#
# # Lex and format the sample input
# puts formatter.format(lexer.lex(sample_input))
