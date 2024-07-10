# _plugins/gdb_lexer.rb
require 'rouge'

module Rouge
  module Lexers
    class Session < RegexLexer
      title "Session"
      desc "Bash session output"
      tag 'session'
      aliases 'session'
      filenames '*.session'

      state :root do
        # Rule for lines beginning with (gdb) followed by any command
        rule /^\$.*/, Generic::Prompt
        rule /\s+/, Text::Whitespace
        rule /-[a-zA-Z]/, Keyword
        rule /\S+/, Text
      end
    end
  end
end

# Sample input to test the lexer
# sample_input = <<~EOF
# $ addr2line -e /path/to/your/executable 0xADDRESS
# $ objdump -d -S /path/to/your/executable
# EOF
#
# # Instantiate the lexer and formatter
# lexer = Rouge::Lexers::Session.new
# formatter = Rouge::Formatters::Terminal256.new
#
# # Lex and format the sample input
# puts formatter.format(lexer.lex(sample_input))
