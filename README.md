# liturgical-markup
Programs for processing my liturgical markup language

## Language definition

Comment lines begin with `#` and are ignored.

Vertical whitespace is not significant.

Heading lines begin with `%`.

Rubric lines begin with `!`.

Scripture references are in square brackets, and verse (or chapter) ranges are indicated with double dashes (like in TeX).

Lines beginning with numnbers (or spaces and numbers) start verses; continuation lines after them begin with spaces.

The symbol `♦` (filled diamond), or `$`, at the end of a line, marks the division of a verse.

## Output

The output format is LaTeX with the package https://ctan.math.utah.edu/ctan/tex-archive/macros/unicodetex/latex/book-of-common-prayer/book-of-common-prayer.pdf
