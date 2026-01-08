# =============================================================================
# .latexmkrc - Latexmk Configuration File
# =============================================================================
# This file configures latexmk for building LaTeX documents.
# See: https://mg.readthedocs.io/latexmk.html
# =============================================================================

# -----------------------------------------------------------------------------
# PDF Generation Mode
# -----------------------------------------------------------------------------
# Use pdflatex for PDF generation
$pdf_mode = 1;

# Alternative: Use LuaLaTeX (uncomment to enable)
# $pdf_mode = 4;
# $lualatex = 'lualatex -shell-escape -interaction=nonstopmode -file-line-error %O %S';

# Alternative: Use XeLaTeX (uncomment to enable)
# $pdf_mode = 5;
# $xelatex = 'xelatex -shell-escape -interaction=nonstopmode -file-line-error %O %S';

# -----------------------------------------------------------------------------
# Compiler Options
# -----------------------------------------------------------------------------
# pdflatex with shell-escape (required for minted)
$pdflatex = 'pdflatex -shell-escape -interaction=nonstopmode -file-line-error %O %S';

# -----------------------------------------------------------------------------
# Output Directory
# -----------------------------------------------------------------------------
# Build artifacts go to the build/ directory
$out_dir = 'build';
$aux_dir = 'build';

# Ensure output directory exists
system("mkdir -p build");

# -----------------------------------------------------------------------------
# Bibliography
# -----------------------------------------------------------------------------
# Use biber for biblatex
$biber = 'biber %O %S';
$bibtex_use = 2;  # Run biber when needed

# -----------------------------------------------------------------------------
# Cleanup Configuration
# -----------------------------------------------------------------------------
# Files to clean with -c (intermediate files)
$clean_ext = 'aux bbl bcf blg fdb_latexmk fls log out run.xml toc lof lot nav snm vrb';

# Files to clean with -C (all generated files including PDF)
$clean_full_ext = 'aux bbl bcf blg fdb_latexmk fls log out run.xml toc lof lot nav snm vrb pdf synctex.gz';

# -----------------------------------------------------------------------------
# Glossaries (if using glossaries package)
# -----------------------------------------------------------------------------
# Uncomment if using the glossaries package
# add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
# add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
# sub run_makeglossaries {
#     my ($base_name, $path) = fileparse($_[0]);
#     return system "makeglossaries -d '$path' '$base_name'";
# }

# -----------------------------------------------------------------------------
# Preview Mode
# -----------------------------------------------------------------------------
# PDF viewer for preview mode (-pv or -pvc)
# macOS
$pdf_previewer = 'open -a Preview %O %S';

# Linux (uncomment one)
# $pdf_previewer = 'evince %O %S';
# $pdf_previewer = 'okular %O %S';
# $pdf_previewer = 'xdg-open %O %S';

# Windows (uncomment)
# $pdf_previewer = 'start %S';

# -----------------------------------------------------------------------------
# Watch Mode Settings
# -----------------------------------------------------------------------------
# Time between checks for updated files (seconds)
$sleep_time = 1;

# Maximum number of runs to prevent infinite loops
$max_repeat = 5;

# -----------------------------------------------------------------------------
# File Dependencies
# -----------------------------------------------------------------------------
# Ensure latexmk recognizes custom file extensions
push @generated_exts, 'glo', 'gls', 'glg', 'acn', 'acr', 'alg';
push @generated_exts, 'run.xml', 'bcf';

# =============================================================================
# End of .latexmkrc
# =============================================================================
