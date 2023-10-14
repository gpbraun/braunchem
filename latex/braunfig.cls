%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  The BRAUN Package
%
%          --  Problem Sheet Typesetting -- 
%
%============================================================%
%
%  GABRIEL P. BRAUN, 2019-2021
%
%============================================================%
%
%  CONTACT: braun.pineschi@gmail.com
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CLASS REQUIREMENTS AND SETUP                   
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { l3keys2e, l3draw, l3graphics, silence }

\ExplSyntaxOn

\tl_const:Nn \c_brauntex_date_tl                 {2022/02/02}
\tl_const:Nn \c_brauntex_version_major_number_tl {7}
\tl_const:Nn \c_brauntex_version_minor_number_tl {0}
\tl_const:Nn \c_brauntex_version_subrelease_tl   {a}
\tl_const:Nx \c_brauntex_version_number_tl
	{
			\c_brauntex_version_major_number_tl .
			\c_brauntex_version_minor_number_tl
	}
\tl_const:Nx \c_brauntex_version_tl
	{
		\c_brauntex_version_number_tl
		\c_brauntex_version_subrelease_tl
	}
\tl_const:Nn \c_brauntex_info_tl { BraunTex~ Class }

\ProvidesExplClass
	{ braunfigure }
	{ \c_brauntex_date_tl    }
	{ \c_brauntex_version_tl }
	{ \c_brauntex_info_tl    }

%============================================================%
%   FILTERED WARNINGS
%============================================================%

\WarningFilter{ latex }            { Font~shape }
\WarningFilter{ latex }            { Unused~global~option(s) }
\WarningFilter{ latex }            { \KOMAScriptVersion }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   MACROS                 
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   VARIANTS OF KERNEL FUNCTIONS
%============================================================%

\cs_generate_variant:Nn \box_autosize_to_wd_and_ht:Nnn {NVV}
\cs_generate_variant:Nn \dim_compare:nNnF {vNVF}
\cs_generate_variant:Nn \draw_linewidth:n {V}
\cs_generate_variant:Nn \coffin_typeset:Nnnnn {NnVnV}
\cs_generate_variant:Nn \color_fill:n {V}
\cs_generate_variant:Nn \color_stroke:n {V}
\cs_generate_variant:Nn \color_select:n {e}
\cs_generate_variant:Nn \color_select:n     {V}
\cs_generate_variant:Nn \clist_put_right:Nn {Ne}
\cs_generate_variant:Nn \seq_use:Nnnn {cvvv}
\cs_generate_variant:Nn \skip_vertical:n {V}
\cs_generate_variant:Nn \prop_get:NnNTF {NVNTF}
\cs_generate_variant:Nn \vcoffin_set:Nnn {NVn}

%============================================================%
%   GENERAL USAGE
%============================================================%

\cs_set:Npn \BraunNoWarning % Avoid badness errors
    { 
        \dim_set_eq:NN \vfuzz    \c_max_dim
        \dim_set_eq:NN \hfuzz    \c_max_dim
        \int_set_eq:NN \hbadness \c_max_int
        \int_set_eq:NN \vbadness \c_max_int
    }

\cs_set_eq:NN \BraunVFill \tex_vfill:D

%============================================================%
%   BASE CLASS
%============================================================%

\LoadClass [ 
    border  = 1cm, 
    convert = 
        { 
            command = 
                \unexpanded{{
                    pdfcrop~ \inname.pdf~ \inname.pdf &&
                    pdf2svg~ \inname.pdf~ \inname.svg
                }}
        }
] 
{ standalone }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CLASS              
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\keys_define:nn { braun }
    {
        language .code:n    = \PassOptionsToPackage {#1} { babel },
        language .initial:n = brazil,

        linewidth .dim_set:N = \g_braun_linewidth_dim,
		linewidth .initial:n =  0.4pt,
    }

% #1 -> module
% #2 -> keys
\NewDocumentCommand \braunsetup { o m } 
    { \exp_args:Ne \keys_set:nn { braun \IfValueT {#1} {/#1} } {#2} }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   FONTS       
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\keys_define:nn { braun }
    {
        familydefault .tl_set:N = \g_braun_family_default_tl,

        font .tl_set:N  = \g_braun_font_tl,
        font .initial:n = ptsans,

        emph .code:n = \cs_gset:Npn \emph ##1 { { #1 ##1 } },
    }

\cs_set:Nn \braun_select_font:
    {
        %% font names
        \RequirePackage { anyfontsize }
        \str_case:Vn \g_braun_font_tl
            {
                { lmodern }
                { 
                    \RequirePackage { lmodern  }
                }
                { ptsans }
                {
                    \RequirePackage { lmodern }
                    \RequirePackage [ scaled ] { PTSans }
                }
                { paratype }
                {
                    \RequirePackage { paratype }
                    \RequirePackage { eulervm  }
                }  
                { helvetica }
                { 
                    \RequirePackage { lmodern }
                    \RequirePackage [ scaled  ] { helvet }
                }          
            }
        % family default
        \str_case:Vn \g_braun_family_default_tl
            {
                { rm } { \cs_gset_eq:NN \familydefault \rmdefault }
                { sf } { \cs_gset_eq:NN \familydefault \sfdefault }
            }
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BASIC 
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   TYPOGRAPHY
%============================================================%

\RequirePackage [T1] { fontenc }
%\RequirePackage { microtype }

%============================================================%
%   MATH
%============================================================%

\RequirePackage { mathtools, amssymb, textcomp, marvosym }

\numberwithin { equation     } { section }
\mathtoolsset { showonlyrefs }

\cs_set_eq:NN \degree \textdegree

%============================================================%
%   SI UNITS
%============================================================%

\RequirePackage { siunitx }

\sisetup 
    { 
        range-phrase = { ~a~ }, 
        list-final-separator = { ~e~ }, 
        locale = FR,
    }

\cs_set_eq:NN \pu \mathrm

%============================================================%
%   CHEMISTRY
%============================================================%

\RequirePackage [version=4] { mhchem }

\RequirePackage { braunchem }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   DRAWING
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\PassOptionsToPackage { table } { xcolor }

\RequirePackage{ tikz }

%============================================================%
%   PLOTTING
%============================================================%

\RequirePackage{ pgfplots }

\keys_define:nn { braun/draw/plot }
    { 
        unknown .code:n = \exp_args:Ne \pgfplotsset { \l_keys_key_tl = #1 },
    }

\pgfqkeys { /pgf/number~format }
    {
        set~thousands~separator = {},
        set~decimal~separator = {,\!},
    }

\pgfplotsset
    {
        compat = 1.17,
        samples = 150,
        legend~cell~align = left,
        every~axis~plot/.append~style = {very~thick},
        every~axis~plot/.append~style = {mark=none},
        every~axis~plot/.append~style = {mark~options={fill=white}},
        bar~cycle~list/.style = 
        {
            /pgfplots/cycle~list=
            { 
                {blue, fill=blue!20}, 
                {red, fill=red!20}, 
                {green, fill=green!20},
                {purple, fill=purple!20}, 
            },
        }
    }

\tikzstyle{every~pin}=[draw=black]

\AtBeginDocument 
    {
        \usepgfplotslibrary{groupplots, fillbetween}
        \usetikzlibrary
            {
                calc,
                shapes.geometric,
                decorations.text, 
                decorations.pathreplacing,
                decorations.markings,
                decorations.pathmorphing,
                arrows.meta,
            }
    }

%============================================================%
%   COLOR PALLETS
%============================================================%

\definecolor { blue   } { HTML } { 0d6efd }
\definecolor { indigo } { HTML } { 6610f2 }
\definecolor { purple } { HTML } { 6f42c1 }
\definecolor { pink   } { HTML } { d63384 }
\definecolor { red    } { HTML } { dc3545 } 
\definecolor { orange } { HTML } { fd7e14 } 
\definecolor { yellow } { HTML } { ffc107 } 
\definecolor { green  } { HTML } { 198754 } 
\definecolor { teal   } { HTML } { 20c997 } 
\definecolor { cyan   } { HTML } { 0dcaf0 } 
\definecolor { lime   } { HTML } { 84cc16 }

% GRAYSCALE
\definecolor { gray-100 } { HTML } { f8f9fa }
\definecolor { gray-200 } { HTML } { e9ecef }
\definecolor { gray-300 } { HTML } { dee2e6 }
\definecolor { gray-400 } { HTML } { ced4da }
\definecolor { gray-500 } { HTML } { adb5bd } 
\definecolor { gray-600 } { HTML } { 6c757d } 
\definecolor { gray-700 } { HTML } { 495057 } 
\definecolor { gray-800 } { HTML } { 343a40 } 
\definecolor { gray-900 } { HTML } { 212529 } 

% CORES DOS BLOCOS
\colorlet{ s-block } { blue   }
\colorlet{ p-block } { yellow }
\colorlet{ d-block } { red    }
\colorlet{ f-block } { purple }
 
\pgfplotscreateplotcyclelist { braun-pallet }
    {
        { blue },
        { red },
        { green },
    }
\pgfplotsset
    {
        cycle~list~name = braun-pallet,
    }

%============================================================%
%   PLOTTING
%============================================================%

\RequirePackage{ pgfplots }

\keys_define:nn { braun/draw/plot }
    { 
        unknown .code:n = \exp_args:Ne \pgfplotsset { \l_keys_key_tl = #1 },
    }

\pgfqkeys { /pgf/number~format }
    {
        set~thousands~separator = {},
        set~decimal~separator = {,\!},
    }

\pgfplotsset
    {
        compat = 1.17,
        samples = 150,
        legend~cell~align = left,
        every~axis~plot/.append~style = {very~thick},
        every~axis~plot/.append~style = {mark=none},
        every~axis~plot/.append~style = {mark~options={fill=white}},
    }

\tikzstyle{every~pin}=[draw=black]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PROCESS OPTIONS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProcessKeysOptions { braun }

\braun_select_font:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   LANGUAGE
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { csquotes, babel }

\AtBeginEnvironment{quote}{\small}

\cs_set_eq:NN \textbackslash \relax

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ExplSyntaxOff
