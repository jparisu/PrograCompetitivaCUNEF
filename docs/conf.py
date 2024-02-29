project = 'PrograCompetitivaCunef'
author = 'PCriado'

extensions = [
    'sphinx.ext.autodoc',
    'myst_parser',
    'sphinx.ext.todo',

]
html_theme = 'sphinx_rtd_theme'


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# The spelling list filename.
spelling_word_list_filename=['spelling/spelling_wordlist.txt']

# Change tab title
release = '0.0.0'
html_title = f"{project} {release} Documentation"

# Include to-do items
todo_include_todos = True
