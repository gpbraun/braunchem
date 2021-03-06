%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  ______                       _____ _                      %
%  | ___ \                     /  __ \ |                     %
%  | |_/ /_ __ __ _ _   _ _ __ | /  \/ |__   ___ _ __ ___    %
%  | ___ \ '__/ _` | | | | '_ \| |   | '_ \ / _ \ '_ ` _ \   %
%  | |_/ / | | (_| | |_| | | | | \__/\ | | |  __/ | | | | |  %
%  \____/|_|  \__,_|\__,_|_| |_|\____/_| |_|\___|_| |_| |_|  %
%                                                            %
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

\LoadClass [tikz] { standalone }

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

\RequirePackage { mathtools, amssymb, textcomp }

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
        round-mode = figures,
        round-precision = 3,
        drop-zero-decimal,
    }

\cs_set_eq:NN \pu \mathrm

%============================================================%
%   CHEMISTRY
%============================================================%

\RequirePackage [version=4] { mhchem }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   DRAWING
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{ tikz }

\cs_gset_eq:NN \legacydefinecolor \definecolor
\cs_gset_eq:NN \legacycolor       \color

% redefines \definecolor to use l3color
\DeclareDocumentCommand \definecolor { m m m }
    { 
        \legacydefinecolor {#1} {#2} {#3} 
        \color_set:nnn     {#1} {#2} {#3} 
    }

% % redefines \color to use l3color
% \DeclareDocumentCommand \color { o m } { \color_select:e {#2} }

% \cs_set:Npn \legacycolor
%     {
%         \cs_set_eq:NN \color \legacycolor
%     }

%============================================================%
%   COLOR PALLETS
%============================================================%

% #1 -> color pallet name
\cs_set:Npn \SetColorPallet #1
    {
        \str_case:nn {#1}
            {
                { classic }
                { 
                    \definecolor { color-1 } { HTML } { 00345A } % PrussianBlue
                    \definecolor { color-2 } { HTML } { C21E56 } % RoseRed
                    \definecolor { color-3 } { HTML } { FDD166 } % PensiYellow
                    \definecolor { color-4 } { HTML } { 009F6B } % GreenNCS
					\definecolor { color-5 } { HTML } { F5AB00 } % Darker Yellow
                    \definecolor { gray-1  } { HTML } { 727176 } 
                    \definecolor { gray-2  } { HTML } { 87868A } 
                    \definecolor { gray    } { HTML } { 87868A } 
                }   
                { boostrap }
                { 
                    \definecolor { color-1 } { HTML } { 0d6efd } % PrussianBlue
                    \definecolor { color-2 } { HTML } { d63384 } % RoseRed
                    \definecolor { color-3 } { HTML } { ffc107 } % PensiYellow
                    \definecolor { color-4 } { HTML } { 20c997 } % GreenNCS
					\definecolor { color-5 } { HTML } { F5AB00 } % Darker Yellow
                    \definecolor { gray-1  } { HTML } { 727176 } 
                    \definecolor { gray-2  } { HTML } { 87868A } 
                    \definecolor { gray    } { HTML } { 87868A } 
                }            
            }
        \pgfplotscreateplotcyclelist { braun-pallet }
            {
                { color-1 },
                { color-2 },
                { color-3 },
                { color-4 },
            }
        \pgfplotsset
            {
                cycle~list~name = braun-pallet,
            }
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

%============================================================%
%   DRAWING KEYS
%============================================================%

\keys_define:nn { braun/color }
    {
        legacy .bool_set:N = \l_braun_color_legacy_bool,
        legacy .initial:n  = false,
        legacy .default:n  = true,

        pallet .code:n    = \SetColorPallet {#1},
        pallet .initial:n = boostrap,
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   FIGURES
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { svg }

\keys_define:nn { braun/graphics }
	{
        fps .code:n = { \cs_set_protected:Npn \fps@figure {#1} },
        fps .initial:n = H,

        width .dim_set:N = \l_braun_graphics_width_dim,
		width .initial:n = 5cm,

		height .dim_set:N = \l_braun_graphics_height_dim,
		height .initial:n = 4cm,

        path .tl_set:N = \g_braun_graphics_path_tl,
        path .initial:n = ,

	}

% #1 -> coffin
% #2 -> content
\cs_set:Nn \braun_graphics_box:Nn
{ 
    \hcoffin_set:Nn #1
        {
            \group_begin:
                \hbox_set:Nn \l_tmpa_box {#2}
                \box_autosize_to_wd_and_ht:NVV \l_tmpa_box 
                    \l_braun_graphics_width_dim \l_braun_graphics_height_dim 
                \box_use_drop:N \l_tmpa_box
            \group_end:
        }   
}

% #1 -> coffin
% #2 -> figure path
\cs_set:Nn \braun_include_graphics:Nn
    { 
        \file_if_exist:nT { \g_braun_graphics_path_tl / #2 }
            { 
                \braun_graphics_box:Nn #1 
                    { \graphics_include:n { \g_braun_graphics_path_tl / #2 } } 
            }
    }

% #1 -> coffin
% #2 -> svg path
\cs_set:Nn \braun_include_svg:Nn
    { 
        \file_if_exist:nT { \g_braun_graphics_path_tl / #2 }
            { 
                \braun_graphics_box:Nn #1 
                    { \includesvg [pretex=\sffamily] { \g_braun_graphics_path_tl / #2 } } 
            }
    }

\cs_set_eq:NN \legacyincludegraphics \includegraphics

\tl_new:N \l_tmpc_tl

% #1 -> keys: braun/graphics
% #2 -> figure path
\DeclareDocumentCommand \includegraphics { o m }
    { 
        \group_begin:
        \IfValueT {#1} { \keys_set:nn { braun/graphics } {#1} }
        \file_parse_full_name:nNNN {#2} \l_tmpa_tl \l_tmpb_tl \l_tmpc_tl
        \str_case:VnF \l_tmpc_tl
            {
                { .svg }
                { 
                    \file_if_exist_input:nF 
                        { \g_braun_graphics_path_tl / \l_tmpa_tl / \l_tmpb_tl .tex }
                        { \braun_include_svg:Nn \l_tmpa_coffin {#2} }
                }      
            }
            {
                \braun_include_graphics:Nn \l_tmpa_coffin {#2}
            }

        \coffin_typeset:Nnnnn \l_tmpa_coffin {l} {vc} {0pt} {0pt}
        \group_end:
    }

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