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
	{ braun }
	{ \c_brauntex_date_tl    }
	{ \c_brauntex_version_tl }
	{ \c_brauntex_info_tl    }

%============================================================%
%   FILTERED WARNINGS
%============================================================%

\WarningFilter{ hyperref }         { Token~not~allowed~in~a~PDF~string }
\WarningFilter{ typearea }         { Bad~type~area~settings! }
\WarningFilter{ latex }            { Font~shape }
\WarningFilter{ latex }            { Unused~global~option(s) }
\WarningFilter{ latex }            { \KOMAScriptVersion }
\WarningFilter{ scrlayer-scrpage } { \headheight }

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

\tl_const:Nn \c_brauntex_base_class_tl { article }
\exp_args:NV \LoadClass \c_brauntex_base_class_tl

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
%   KOMASCRIPT FEATURES
%============================================================%

\RequirePackage { typearea, scrextend }

\keys_define:nn { braun }
    { unknown .code:n  = \exp_args:NV \KOMAoption \l_keys_key_tl {#1} }

%============================================================%
%   FIGURES AND TABLES 
%============================================================%

\RequirePackage { float, booktabs, array }

\cs_set_eq:NN \endhead \relax
\cs_set_eq:NN \tightlist \relax

\NewDocumentEnvironment { longtable } { O{} m }
	{
		\begin{center}
		\begin{tabular} [] {#2} 
		
	}
	{
		\end{tabular}
		\end{center}
	}

%============================================================%
%   MATH
%============================================================%

\RequirePackage { mathtools, amssymb, textcomp }

\numberwithin { equation     } { section }
\mathtoolsset { showonlyrefs }

\cs_set_eq:NN \degree \textdegree
\cs_set_eq:NN \hbar   \hslash

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
%   BOXES
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\keys_define:nn { braun/box }
    {
        width .dim_set:N = \l_braun_box_width_dim,
        width .initial:n = 2em,

        fill  .tl_set:N  = \l_braun_box_fill_tl,
        fill  .initial:n = white,

        stroke  .tl_set:N  = \l_braun_box_stroke_tl,
        stroke  .initial:n = black,

        align  .tl_set:N  = \l_braun_box_align_tl,
        align  .initial:n = t,

        yshift .dim_set:N  = \l_braun_box_yshift_dim,
        yshift .initial:n  = 0pt,
    }

%============================================================%
%   HEADERS
%============================================================%

\coffin_new:N \l__braun_txta_coffin
\coffin_new:N \l__braun_txtb_coffin

% #1 -> name
% #2 -> code
\NewDocumentCommand \DeclareBraunHeader { m o m o }
	{
		\exp_args:Nc \NewDocumentCommand { \char_uppercase:N #1 Header } { o m }
			{
				\BraunNoWarning
				\skip_vertical:n { 1ex } 
				\group_begin:
					\dim_zero:N \parindent
					\draw_begin:
						\draw_linewidth:V \g_braun_linewidth_dim
						\hcoffin_set:Nn   \l__braun_txta_coffin {##2}
						\hcoffin_set:Nn   \l__braun_txtb_coffin {##1}
						#3
					\draw_end:
				\group_end:
				\skip_vertical:n { 1ex } 
			}
	}

%% BRAUN

\DeclareBraunHeader { braun }
    {
        \draw_path_moveto:n 
            { \linewidth , 0em }
        \draw_path_lineto:n 
            { \coffin_wd:N \l__braun_txta_coffin + 4ex , 0cm }
        \draw_path_corner_arc:nn { 2ex }{ 2ex }
        \draw_path_lineto:n 
            { \coffin_wd:N \l__braun_txta_coffin + 4ex , \coffin_ht:N \l__braun_txta_coffin + 2.5ex }
        \draw_path_corner_arc:nn { 0cm }{ 0cm }
        \draw_path_lineto:n 
            { 0cm , \coffin_ht:N \l__braun_txta_coffin + 2.5ex }
        \draw_path_corner_arc:nn { 2ex }{ 2ex }
        \draw_path_lineto:n 
            { 0cm , 0em }
        \draw_path_lineto:n 
            { \coffin_wd:N \l__braun_txta_coffin + 4ex , 0em }
        \color_fill:n { gray-1!60 }
        \draw_path_use_clear:n { fill, stroke }
        \draw_transform_shift:n 
            { \linewidth - 1em , 1.25ex }
        \draw_coffin_use:Nnn \l__braun_txtb_coffin {r}  {H}
        \draw_transform_shift:n 
            { ( \coffin_wd:N \l__braun_txta_coffin + 4ex ) / 2 - \linewidth + 1em , 0cm }
        \draw_coffin_use:Nnn \l__braun_txta_coffin {hc} {H}
    }
    
%% IME HEADER 1 (PROBLEMS)

\DeclareBraunHeader { IME }
    {
        \skip_horizontal:n { -\marginparsep }
        \draw_path_rectangle:nn 
            { 0cm , 0cm }
            { \linewidth + 2 \marginparsep , \coffin_ht:N \l__braun_txtb_coffin + 1em }
        \color_fill:n { white }
        \draw_path_use_clear:n { stroke, fill }
        \draw_transform_shift:n 
            { \linewidth - \coffin_wd:N \l__braun_txtb_coffin , 0.0cm }
        \draw_path_moveto:n 
            { 0cm , 0cm }
        \draw_path_lineto:n 
            { 0cm , \coffin_ht:N \l__braun_txtb_coffin + 1em }
        \draw_path_use_clear:n { stroke }
        \draw_transform_shift:n 
            { \coffin_wd:N \l__braun_txtb_coffin + \marginparsep , 0.5em }
        \draw_coffin_use:Nnn \l__braun_txtb_coffin {r}  {H}
        \draw_transform_shift:n 
            { -\linewidth , 0cm }
        \draw_coffin_use:Nnn \l__braun_txta_coffin {l} {H}
    }

%% IME HEADER 2 (SECTIONS)

\DeclareBraunHeader { IMEalt }
    {
        \skip_horizontal:n { -\marginparsep }
        \draw_path_rectangle:nn 
            { 0cm  , 0cm }
            { \linewidth + 2 \marginparsep ,  \coffin_ht:N \l__braun_txtb_coffin + 1em }
        \color_fill:n { white }
        \draw_path_use_clear:n { stroke, fill }
        \draw_transform_shift:n 
            { \linewidth / 2 + \marginparsep ,  0.5em }
        \draw_coffin_use:Nnn \l__braun_txta_coffin {hc} {H}
    }

%============================================================%
%   BOXES
%============================================================%

% #1 -> name
% #2 -> code
\NewDocumentCommand \DeclareBraunBox { m o m }
	{
		\exp_args:Nc \NewDocumentCommand { \char_uppercase:N #1 Box } { o m }
			{
				\BraunNoWarning
				\group_begin:
					\dim_zero:N \parindent
					\IfValueT {##1} { \keys_set:nn { braun/box } {##1} }
					\vcoffin_set:NVn \l__braun_txta_coffin \l_braun_box_width_dim
						{ 	
							\color { black }
							\centering
							##2 
						}
					\hcoffin_set:Nn \l_tmpa_coffin
						{
							\draw_begin:
								\draw_linewidth:V \g_braun_linewidth_dim
								\color_stroke:V   \l_braun_box_stroke_tl
								\color_fill:V     \l_braun_box_fill_tl
								#3
							\draw_end:
						}
					\coffin_typeset:NnVnV \l_tmpa_coffin {l} \l_braun_box_align_tl {0pt} \l_braun_box_yshift_dim
				\group_end:
			}
	}

%% ROUND BOX

\DeclareBraunBox { round }
	{
		\draw_path_circle:nn { 0cm, 0cm } { \l_braun_box_width_dim/2 }
		\draw_path_use_clear:n { fill, stroke }
		\draw_coffin_use:Nnn \l__braun_txta_coffin {hc} {vc}
	}

%% SQUARE BOX

\DeclareBraunBox { square }
	{
		\draw_path_rectangle_corners:nn 
			{ -\l_braun_box_width_dim/2 , -\l_braun_box_width_dim/2 }
			{  \l_braun_box_width_dim/2 ,  \l_braun_box_width_dim/2 }
		\draw_path_use_clear:n { fill, stroke }
		\draw_coffin_use:Nnn \l__braun_txta_coffin {hc} {vc}
	}

%============================================================%
%   MINIBOXES
%============================================================%

% #1 -> content
% #2 -> size
\cs_set:Nn \braun_mini_box:nn
	{
		\group_begin:

		\hcoffin_set:Nn \l_tmpa_coffin 
			{
				\draw_begin:
					\draw_path_moveto:n { -#2 +0.2ex, -#2 }
					\draw_path_lineto:n { #2 -0.2ex  , -#2 }
					\draw_path_corner_arc:nn { 0.6ex }{ 0.6ex }
					\draw_path_lineto:n { #2 -0.2ex, #2 }
					\draw_path_corner_arc:nn { 0cm }{ 0cm }
					\draw_path_lineto:n { -#2 +0.2ex, #2 }
					\draw_path_corner_arc:nn { 0.6ex }{ 0.6ex }
					\draw_path_close:
					\color_fill:n { gray-1!60 }
					\draw_path_use_clear:n { fill }
				\draw_end:
			}
		\hcoffin_set:Nn \l_tmpb_coffin {#1}
		\coffin_join:NnnNnnnn \l_tmpa_coffin {hc}{vc} \l_tmpb_coffin {hc}{vc} {0pt} {0pt}

		\coffin_typeset:Nnnnn \l_tmpa_coffin {\l_tmpb_coffin-H}{l} {0pt}{0pt}

		\group_end:
	}

%% FRONT-END

\NewDocumentCommand \MiniBox { m }
	{ \braun_mini_box:nn  { \bfseries\sffamily\small #1 }{0.65em} }

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
            }
        \pgfplotscreateplotcyclelist { braun-pallet }
            {
                { black },
                { color-2 },
                { color-1 },
                { color-5 },
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
        pallet .initial:n = classic,
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PAGE LAYOUT
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { scrlayer-scrpage, multicolrule, caption }

\cs_set:Nn \braun_page_box:
    {
        \vbox_to_zero:n % zero height
            {
                \hbox_to_zero:n % zero width
                    {
                        \draw_begin:
                            \draw_linewidth:V \g_braun_linewidth_dim
                            \skip_horizontal:n 
                                { - \linewidth / 2 - \marginparsep }
                            \draw_path_rectangle:nn 
                                { 0cm , 0cm }
                                { \linewidth + 2 \marginparsep , \textheight + \footskip - 1.5ex }
                            \draw_path_use_clear:n { stroke }
                        \draw_end:
                    }
            }
        \skip_vertical:n { - \headsep - \headheight - 2.1ex }
    }


\keys_define:nn { braun/page }
    {
        headfoot-font .code:n    = \setkomafont { pageheadfoot } {#1},
        headfoot-font .initial:n =  ,

        boxed .bool_set:N = \l_braun_boxed_page_bool ,
        boxed .initial:n  = false,
        boxed .default:n  = true,

        columnsep .dim_set:N = \columnsep,
        columnsep .initial:n = 3em,
    }

%============================================================%
%   CAPTIONS
%============================================================%

\keys_define:nn { braun/page/caption }

    { unknown .code:n = \exp_args:Ne \captionsetup { \l_keys_key_tl = #1 } }

%============================================================%
%   COLUMN SEPARATOR
%============================================================%

\keys_define:nn { braun/page/mcrule }
    { 
        fancy .meta:n = 
            {
                line-style = dashed,
                width      = thick,
                color      = gray-1!60,
            },

        unknown .code:n = \exp_args:Ne \SetMCRule { \l_keys_key_tl = #1 },
    }

%============================================================%
%   HEADER
%============================================================%

\keys_define:nn { braun/page/header }
    {
        sepline .choices:nn = { true, false } 
            {
                \exp_args:Nne \KOMAoption { headsepline }
                    {  
                        \str_if_eq:nnTF {#1} { true } 
                            { \dim_use:N \g_braun_linewidth_dim } { false }
                    }
            },
        sepline .initial:n = false,
        sepline .default:n = true,

        title-sepline .choices:nn = { true, false } 
            {
                \KOMAoption { plainheadsepline } {#1}
            },
        title-sepline .initial:n = false,
        title-sepline .default:n = true,

        font .code:n    = \setkomafont { pagehead } {#1},
        font .initial:n =  ,

        inner  .tl_set:N  = \l_braun_page_ihead_tl ,
        center .tl_set:N  = \l_braun_page_chead_tl ,
        outer  .tl_set:N  = \l_braun_page_ohead_tl ,

        title-inner  .tl_set:N  = \l_braun_page_title_ihead_tl ,
        title-center .tl_set:N  = \l_braun_page_title_chead_tl ,
        title-outer  .tl_set:N  = \l_braun_page_title_ohead_tl ,

        plain .meta:n = 
            { 
                inner  = ,
                center = ,
                outer  = ,
                sepline = false,
                title-inner  = ,
                title-center = ,
                title-outer  = ,
                title-sepline = false,
            },
    }

\ihead 
    [ \tl_use:N \l_braun_page_title_ihead_tl ] 
    { \tl_use:N \l_braun_page_ihead_tl }
\chead
    [   
        \bool_if:NT \l_braun_boxed_page_bool { \braun_page_box: } 
        \tl_use:N \l_braun_page_title_chead_tl
    ]
    {
        \bool_if:NT \l_braun_boxed_page_bool { \braun_page_box: }   
        \tl_use:N   \l_braun_page_chead_tl
    }
\ohead 
    [ \tl_use:N \l_braun_page_title_ohead_tl ] 
    { \tl_use:N \l_braun_page_ohead_tl }

%============================================================%
%   FOOTER
%============================================================%

\keys_define:nn { braun/page/footer }
    {
        sepline .choices:nn = { true, false } 
            {
                \exp_args:Nne \KOMAoption { footsepline }
                    {  
                        \str_if_eq:nnTF {#1} { true } 
                            { \dim_use:N \g_braun_linewidth_dim } { false }
                    }
            },
        sepline .initial:n = false,
        sepline .default:n = true,

        title-sepline .choices:nn = { true, false } 
            {
                \KOMAoption { plainfootsepline } {#1}
            },
        title-sepline .initial:n = false,
        title-sepline .default:n = true,

        font .code:n    = \setkomafont { pagefoot } {#1},
        font .initial:n =  {},

        inner  .tl_set:N  = \l_braun_page_ifoot_tl ,
        center .tl_set:N  = \l_braun_page_cfoot_tl ,
        center .initial:n = { \thepage },
        outer  .tl_set:N  = \l_braun_page_ofoot_tl ,

        title-inner  .tl_set:N  = \l_braun_page_title_ifoot_tl ,
        title-center .tl_set:N  = \l_braun_page_title_cfoot_tl ,
        title-center .initial:n = { \thepage },
        title-outer  .tl_set:N  = \l_braun_page_title_ofoot_tl ,

        plain .meta:n = 
            { 
                inner  = ,
                center = {\thepage},
                outer  = ,
                sepline = false,
                title-inner  = ,
                title-center = {\thepage},
                title-outer  = ,
                title-sepline = false,
            },
    }

\ifoot 
    [ \tl_use:N \l_braun_page_title_ifoot_tl ] 
    { \tl_use:N \l_braun_page_ifoot_tl       }
\cfoot 
    [ \tl_use:N \l_braun_page_title_cfoot_tl ] 
    { \tl_use:N \l_braun_page_cfoot_tl       }
\ofoot 
    [ \tl_use:N \l_braun_page_title_ofoot_tl ] 
    { \tl_use:N \l_braun_page_ofoot_tl       }

\ModifyLayer [ addvoffset = -0.7ex ] {       scrheadings.foot.above.line }
\ModifyLayer [ addvoffset = -0.7ex ] { plain.scrheadings.foot.above.line }

%============================================================%
%   SECTIONS
%============================================================%

\keys_define:nn { braun/page/section }
	{
		name .tl_set:N = \l_braun_page_section_type_tl,
		name .initial:n = latex,
	}

\cs_set_eq:NN \legacysection \section

\cs_set:Nn \braun_ghost_section: { \subsection*{} \skip_vertical:n {-3em} }

\counterwithout * { subsection } { section }
\counterwithout * { subsubsection } { subsection }

\RenewDocumentCommand \section { s m }
	{
        \IfBooleanF {#1} { \refstepcounter { section } }
        \group_begin:
		\braun_ghost_section: 

        \str_case:Vn \l_braun_page_section_type_tl
			{
				{ latex }
				{
					\Large \textbf {#2}
				}
				{ IME }
				{
					\skip_vertical:n {-1em}
					\IMEaltHeader 
						{ 
							\bfseries \normalsize  \text_uppercase:n {#2} 
						} 
				}
				{ ITA }
				{
					\begin{center}
						\bfseries \normalsize \text_uppercase:n {#2} 
						\BraunHRule
					\end{center}
				}
			}
        \group_end:
	}

% \cs_set:Nn \braun_firstsection:n
% 	{
% 		\str_case:Vn \l_braun_page_section_type_tl
% 			{
% 				{ latex }
% 				{
% 					\Large \textbf {#2}
% 				}
% 				{ IME }
% 				{
% 					\skip_vertical:n {-1em}
% 					\IMEaltHeader 
% 						{ 
% 							\bfseries \normalsize  \text_uppercase:n {#2} 
% 						} 
% 				}
% 			}
		
% 	}

% \cs_set:Nn \braun_midsection:n
% 	{
% 		\str_case:Vn \l_braun_page_section_type_tl
% 			{
% 				{ latex }
% 				{
% 					\Large \textbf {#2}
% 				}
% 				{ IME }
% 				{
% 					\skip_vertical:n {-1em}
% 					\IMEaltHeader 
% 						{ 
% 							\bfseries \normalsize  \text_uppercase:n {#2} 
% 						} 
% 				}
% 			}
		
% 	}

%============================================================%
%   PAGE STYLE TEMPLATES
%============================================================%

\keys_define:nn { braun/page }
    {
        IME .meta:n = 
            {
                header/plain,
                footer/plain,
                boxed = true,
                section/name = IME,
            }
    }

\pagestyle { scrheadings }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   TITLE
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   TITLE ELEMENTS
%============================================================%

% #1 -> sequence variable
% #2 -> separation
\cs_set:Nn \braun_select_sep:Nn
    {
        \str_case:nn {#2}
            {
                { csv    } { \seq_use:Nn #1   { ,~  } }
                { break  } { \seq_use:Nn #1   { \\  } }
				{ normal } { \seq_use:Nnnn #1 { ~e~ } { ,~ } { ,~e~ } }
            }
    }
\cs_generate_variant:Nn \braun_select_sep:Nn {cv}
\cs_generate_variant:Nn \braun_select_sep:Nn {cn}

% #1 -> text input
% #2 -> text case
\cs_set:Nn \braun_select_case:nn
    {
        \str_case:nnF {#2}
            {
                { upper } { \text_uppercase:n {#1} }
                { lower } { \text_lowercase:n {#1} }
                { title } { \text_titlecase:n {#1} }
                { first } { \text_titlecase_first:n {#1} }
            } {#1}
    }
\cs_generate_variant:Nn \braun_select_case:nn {ev}

% #1 m -> title element name
\NewDocumentCommand \NewTitleElement { o m }
    {
		\seq_new:c  { l_braun_title_#2_value_seq  }
		\bool_new:c { l_braun_title_#2_input_bool }
        \keys_define:nn { braun/maketitle/#2 }
            {
                value .code:n = 
					{ 
						\bool_if:cT { l_braun_title_#2_single_bool }
							{ \seq_clear:c { l_braun_title_#2_value_seq } }
						\seq_put_right:cn { l_braun_title_#2_value_seq } {##1} 
					},
				
				single-value .bool_set:c  = { l_braun_title_#2_single_bool },
				single-value .initial:n   = false,
				single-value .default:n   = true,

                font .tl_set:c   = { l_braun_title_#2_font_tl },

                case .choices:nn = { upper, lower, title, first, none }
                    { \tl_set:cn { l_braun_title_#2_case_tl } {##1} },
                case .initial:n  = first,

                sep .choices:nn = { normal, csv, break }
                    { \tl_set:cn { l_braun_title_#2_sep_tl } {##1} },
                sep .initial:n  = normal,

                sort .bool_set:c = { l_braun_title_#2_sort_bool },
                sort .initial:n  = false,
				sort .default:n  = true,

                pre-text  .tl_set:c = { l_braun_title_#2_pre_text_tl  },
				post-text .tl_set:c = { l_braun_title_#2_post_text_tl },

                before-skip .skip_set:c = { l_braun_title_#2_before_skip },
                before-skip .initial:n  = 0.5em,
				after-skip  .skip_set:c = { l_braun_title_#2_after_skip  },
                after-skip  .initial:n  = 0.5em,
            }
		% Change default keys for the title element
		\IfNoValueF {#1} { \keys_set:nn { braun/maketitle/#2 } {#1} }
        % Set the title element value
        \cs_gset:cpn {#2} ##1 
			{  
				\bool_set_true:c { l_braun_title_#2_input_bool }
				\keys_set:nn { braun/maketitle/#2 }{ value = \exp_not:n {##1} } 
				% LaTeX2e compatibility
				\cs_if_exist:cT {@#2} { \cs_set:cpn {@#2} {##1} } 
			}
        % Print title element value
      	\cs_new:cpn { Print \char_uppercase:N #2 }
            {
				\bool_if:NTF \l_braun_if_maketitle_bool
				{ % inside \maketitle
					\use:c { braun_maketitle_print_#2 }
				}
				{ % outside \maketitle
					\seq_if_empty:cF { l_braun_title_#2_value_seq }
						{
							\braun_select_sep:cn 
								{ l_braun_title_#2_value_seq } { normal } 
						}
				}
            }
		% Print title element value inside \maketitle
		\cs_new:cpn { braun_maketitle_print_#2 }
            {
				\seq_if_empty:cF { l_braun_title_#2_value_seq }
                    {
						\group_begin:
							\dim_compare:vNVF 
								{ l_braun_title_#2_before_skip } = \c_zero_dim
								{
									\skip_vertical:c 
										{ l_braun_title_#2_before_skip }
								}
							\exp_not:n 
								{ \tl_use:c { l_braun_title_#2_font_tl } }
							\tl_use:c  { l_braun_title_#2_pre_text_tl } 
							\braun_select_case:ev
								{ 
									\braun_select_sep:cv
										{ l_braun_title_#2_value_seq } 
										{ l_braun_title_#2_sep_tl    } 
								} 
								{ l_braun_title_#2_case_tl  }
							\tl_use:c { l_braun_title_#2_post_text_tl } 
							\dim_compare:vNVF 
								{ l_braun_title_#2_before_skip } = \c_zero_dim
								{
									\skip_vertical:c 
										{ l_braun_title_#2_after_skip }
								}
						\group_end:
                    }
				\cs_undefine:c { #2 }
			}
    }

%% DEFAULT TITLE ELEMENTS

\NewTitleElement 
	[ font = \LARGE\bfseries ] 
	{ title }

\NewTitleElement 
	[ font = \large ]
	{ subtitle }

\NewTitleElement 
	[ font = \large  ]
	{ author }

\NewTitleElement 
	[ sep = break ]
	{ affiliation }

\NewTitleElement 
	[ case = none, single-value ]
	{ date }

\NewTitleElement 
	[ case = lower, font = \ttfamily , before-skip = 0pt, after-skip = 0pt, pre-text = \textnormal{Contato:~} ]
	{ contact }

%============================================================%
%   LOGO
%============================================================%

\seq_new:N \g_braun_logo_value_seq

\keys_define:nn { braun/maketitle/logo }
	{
		value .code:n = { \seq_put_right:Nn \g_braun_logo_value_seq {#1} },

		height .dim_set:N = \l_braun_logo_height_dim ,
		height .initial:n = 2cm,

		width .dim_set:N = \l_braun_logo_width_dim ,
		width .initial:n = 2cm,
	}

%% SET LOGO

% #1 -> logo name/value
\cs_set:Npn \logo #1
    { \keys_set:nn { braun/maketitle/logo } { value = #1 } }

% #1 -> qrcode link
\cs_set:Npn \qrcode #1
    { 
        \RequirePackage { qrcode }
        \seq_put_right:Nn \g_braun_logo_value_seq { \qrcode {#1} }
    }

\coffin_new:N \l_braun_title_logo_r_coffin
\coffin_new:N \l_braun_title_logo_l_coffin

% #1 -> coffin to revieve logo
\cs_set:Npn \braun_set_logo_coffin:N #1
	{
		\group_begin:
			\seq_gpop_left:NNT \g_braun_logo_value_seq \l_tmpa_tl
				{
					\braun_set_logo_box:N \l_tmpa_box
					\hcoffin_gset:Nn #1 { \box_use_drop:N \l_tmpa_box }
				}
		\group_end:
	}
	
%% PRINT LOGO

% #1 -> box to recieve logo
\cs_set:Npn \braun_set_logo_box:N #1
{
    \hbox_set:Nn #1
        {
            \group_begin:
                \prop_get:NVNTF \l_braun_logos_prop \l_tmpa_tl \l_tmpb_tl 
                    { \tl_use:N \l_tmpb_tl } 
                    { \tl_use:N \l_tmpa_tl }
            \group_end:
        }
    \box_autosize_to_wd_and_ht:NVV #1 \l_braun_logo_width_dim \l_braun_logo_height_dim
}

% #1 -> logo name/value
\cs_new:Npn \PrintLogo #1 
    {
        \group_begin:
            \braun_set_logo_box:N \l_tmpa_box
            \hcoffin_set:Nn       \l_tmpa_coffin { \box_use_drop:N \l_tmpa_box }
            \coffin_typeset:N     \l_tma_coffin  {l} {H} {0pt} {0pt}
        \group_end:
    }

%% PREDEFINED LOGOS

\prop_const_from_keyval:Nn \l_braun_logos_prop
	{
		pensi   = \file_input:n { pensi-logo.tex },
		ime     = \graphics_include:n { ime-logo.pdf },
		ita     = \graphics_include:n { ita-logo.pdf },
        ita-alt = \graphics_include:n { ita-logo-alt.pdf },
	}

%============================================================%
%   PRINT TITLE
%============================================================%

\keys_define:nn { braun/maketitle }
	{
		align .choices:nn = { c, l, r }
			{ \tl_set:Nn \l_braun_title_align_tl {#1} },
		align .initial:n  = c,

		print .clist_set:N = \l_braun_title_print_clist,
		print .initial:n   = { title, subtitle, author, affiliation, date },

		pre-text  .tl_set:N = \l_braun_title_pre_text_tl,
		post-text .tl_set:N = \l_braun_title_post_text_tl,

		toprule .bool_set:N = \l_braun_title_toprule_bool,
		toprule .initial:n  = false,
		toprule .default:n  = true,
		
		botrule .bool_set:N = \l_braun_title_botrule_bool,
		botrule .initial:n  = false,
		botrule .default:n  = true,

		before-skip .skip_set:N = \l_braun_title_before_skip,
		before-skip .initial:n  = 0.5em,
		after-skip  .skip_set:N = \l_braun_title_after_skip,
		after-skip  .initial:n  = 0.5em,
	}

\cs_set:Npn \BraunNoWarning
    { % avoid badness errors
        \dim_set_eq:NN \vfuzz    \c_max_dim
        \dim_set_eq:NN \hfuzz    \c_max_dim
        \int_set_eq:NN \hbadness \c_max_int
        \int_set_eq:NN \vbadness \c_max_int
    }

% #1 -> footnote text
\cs_set:Npn \BraunThanks #1
    { % equivalent to \thanks
		\tl_if_blank:nF {#1}
		{
			\group_begin:
				\cs_set:Npn \thefootnote { \ensuremath { \star } }
				\footnotetext [ 0 ] {#1}
			\group_end:
		}
		\cs_undefine:N \BraunThanks % save memory
    }

\cs_set:Npn \BraunHRule
    { % print horizontal rule
		\group_begin:
			\BraunNoWarning
			\dim_zero:N \parindent
			\skip_vertical:n {1pt}
			\draw_begin:
				\draw_linewidth:V \g_braun_linewidth_dim
				\draw_path_moveto:n { 0cm , 0cm }
				\draw_path_lineto:n { \linewidth , 0cm }
				\draw_path_use_clear:n { stroke }
			\draw_end:
			\skip_vertical:n {1pt}
		\group_end:
    }

% #1 -> content
\cs_set_protected:Npn \BraunSingleColumn #1
    { \legacy_if:nTF { @twocolumn } { \twocolumn [#1] } {#1} }

%% MAKETITLE COMMAND

\coffin_new:N \l_braun_title_coffin
\bool_new:N   \l_braun_if_maketitle_bool

\RenewDocumentCommand \maketitle { o }
    {
        \group_begin:
			\bool_set_true:N \l_braun_if_maketitle_bool
			\BraunNoWarning
			\dim_zero:N  \parindent
			\dim_gzero:N \@topnum % Prevents figures from going at top of page.
			% Set keys
			\IfNoValueF {#1} { \keys_set:nn { braun/maketitle } {#1} }
			% Logo coffins
			\str_if_eq:VnTF \l_braun_title_align_tl {r}
				{ % frist logo on the right
					\braun_set_logo_coffin:N \l_braun_title_logo_l_coffin
					\braun_set_logo_coffin:N \l_braun_title_logo_r_coffin
				}
				{ % frist logo on the left
					\braun_set_logo_coffin:N \l_braun_title_logo_r_coffin
					\braun_set_logo_coffin:N \l_braun_title_logo_l_coffin
				}		
			% Main title coffin
			\vcoffin_set:Nnn \l_braun_title_coffin
				{ \textwidth }
				{
					\str_case:Vn \l_braun_title_align_tl
						{
							{ c } { \centering 	 }
							{ l } { \raggedright }
							{ r } { \raggedleft  }
						}
					%% Print title elements specified by \l_braun_title_print_clist
					\clist_map_inline:Nn \l_braun_title_print_clist 
						{ \use:c { braun_maketitle_print_##1 } }
				}
			% Join coffins
			\coffin_join:NnnNnnnn \l_braun_title_coffin {vc} {r}	
				\l_braun_title_logo_r_coffin {vc} {r} {0pt} {0pt}
			\coffin_join:NnnNnnnn \l_braun_title_coffin {vc} {l}	
				\l_braun_title_logo_l_coffin {vc} {l} {0pt} {0pt}
			% Print title
			\BraunSingleColumn
				{
					\tl_use:N        \l_braun_title_pre_text_tl
					\bool_if:NT      \l_braun_title_toprule_bool { \BraunHRule }
					\skip_vertical:V \l_braun_title_before_skip

					\coffin_typeset:Nnnnn \l_braun_title_coffin {l} {vc} {0pt} {0pt}

					\skip_vertical:V \l_braun_title_after_skip
					\bool_if:NT      \l_braun_title_botrule_bool { \BraunHRule }
					\tl_use:N        \l_braun_title_post_text_tl

					\skip_vertical:n { 3em }
				}
			\bool_if:NT \l_braun_title_contact_input_bool
				{ \BraunThanks { \PrintContact } }
        \group_end:
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
        %% Painel Pensi fix
        \str_case:Vn \l_tmpa_tl
            {
                { /uploads }
                {
                    \braun_include_graphics:Nn \l_tmpa_coffin {../images/ \l_tmpb_tl \l_tmpc_tl}
                }
            }

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

\RenewDocumentEnvironment { figure } {} 
    { 
        \group_begin:
        \cs_set:Npn \caption ##1 { \relax }
        \begin{center} 
        
    } 
    { 
        \end{center} 
        \group_end:
    }

\RenewDocumentEnvironment { table  } {} 
    { 
        \group_begin:
        \cs_set:Npn \caption ##1 { \relax }
        \begin{center} 
    } 
    { 
        \end{center} 
        \group_end:
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   ELEMENTS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   GET PROPERTY FROM ELEMENT SYMBOL/NUMBER
%============================================================%

% #1 -> element symbol
% #2 -> property
\cs_new:Nn \elements_get_property_S:nn % get from symbol
	{ \prop_item:cn { c_elements_#1_prop } {#2} }
\cs_generate_variant:Nn \elements_get_property_S:nn {nV}

% #1 -> element atomic number
% #2 -> property
\cs_new:Nn \elements_get_property_Z:nn % get from number
	{ 
		\prop_item:cn 
			{ c_elements_ \clist_item:Nn \c_elements_clist {#1} _prop } {#2} 
	}
\cs_generate_variant:Nn \elements_get_property_Z:nn {nV}

% #1 -> element symbol/atomic number
% #2 -> property
\cs_new:Npn \GetElementProperty #1 #2 % get from symbol or number
	{
		\regex_match:nnTF {\d} {#1}
			{ \elements_get_property_Z:nn {#1}{#2} }
			{ \elements_get_property_S:nn {#1}{#2} }
	}

%============================================================%
%   ORGANIZE ELEMENT LIST
%============================================================%

\clist_new:N \l__mendeleev_organize_tmp_clist

% #1 -> clist with elements
\cs_set:Nn \mendeleev_organize_elements:N
	{
		\clist_map_inline:Nn #1
			{
				\clist_put_right:Ne \l__mendeleev_organize_tmp_clist 
					{ \elements_get_property_S:nn {##1} { number } }
			}
		\clist_remove_duplicates:N \l__mendeleev_organize_tmp_clist
		\clist_sort:Nn \l__mendeleev_organize_tmp_clist
			{
				\int_compare:nNnTF { ##1 } > { ##2 }
					{ \sort_return_swapped: }
					{ \sort_return_same: }
			}
		\clist_set_eq:NN #1 \l__mendeleev_organize_tmp_clist
	}

%============================================================%
%   PRINT ELEMENT TABLE
%============================================================%

% #1 -> elements clist
\cs_set:Npn \MolTable #1
	{
		\begin{center}
		\group_begin:
			\clist_set:Nn \l_tmpa_clist {#1}
			%% SORTING
			\bool_if:NT \l_ptable_row_sort_bool
				{ \mendeleev_organize_elements:N \l_tmpa_clist  }
			%% SPLIT COLUMNS
			\legacy_if:nTF { @twocolumn } 
				{ \tl_set_eq:NN \l_tmpb_clist \l_tmpa_clist }
				{ % split element list in two
					\bool_while_do:nn 
						{ 
							\int_compare_p:n 
								{ 
									\clist_count:N \l_tmpa_clist > 
									\clist_count:N \l_tmpb_clist 
								} 
						}
						{
							\clist_pop:NNT \l_tmpa_clist \l_tmpa_tl
								{ \clist_put_right:NV \l_tmpb_clist \l_tmpa_tl }
						}
				}
			%% TABLE
			\exp_args:Nx \tabular 
				{ 		
					\legacy_if:nTF { @twocolumn } 
						{
							c 
							S[ table-format = 2   ] 
							S[ 
								round-mode = places,
								round-precision = 2,
								table-format = 3.2, 
								drop-zero-decimal = false 
							]
						}
						{
							c 
							S[ table-format = 2   ] 
							S[ 
								round-mode = places,
								round-precision = 2,
								table-format = 3.2, 
								drop-zero-decimal = false 
							]
							c 
							S[ table-format = 2   ] 
							S[ 
								round-mode = places,
								round-precision = 2,
								table-format = 3.2, 
								drop-zero-decimal = false 
							]
						}
				}
				\toprule
				\legacy_if:nTF { @twocolumn } 
					{ % top header with one column
						{ Elemento    } \c_alignment_token 
						{ Número      } \c_alignment_token 
						{ Massa~Molar } 
					}
					{ % top header with two columns
						{ Elemento    } \c_alignment_token 
						{ Número      } \c_alignment_token 
						{ Massa~Molar } \c_alignment_token 
						{ Elemento    } \c_alignment_token 
						{ Número      } \c_alignment_token 
						{ Massa~Molar }
					}
				\tex_cr:D
				\legacy_if:nTF { @twocolumn } 
					{ % top header with one column
						{ Químico }                   \c_alignment_token 
						{ Atômico }                   \c_alignment_token 
						{ ( \unit { g.mol^{-1} } ) } 
					}
					{  % top header with two columns
						{ Químico }                   \c_alignment_token 
						{ Atômico }                   \c_alignment_token 
						{ ( \unit { g.mol^{-1} } ) }  \c_alignment_token  
						{ Químico }                   \c_alignment_token 
						{ Atômico }                   \c_alignment_token 
						{ ( \unit { g.mol^{-1} } ) } 
					}
				\tex_cr:D
				\midrule 
				\bool_do_until:nn { \clist_if_empty_p:N \l_tmpb_clist }
					{
						\legacy_if:nTF { @twocolumn } 
							{
								\elements_ita_ptable_row:N \l_tmpb_clist
							}
							{
								\elements_ita_ptable_row:N \l_tmpb_clist 
								\c_alignment_token
								\elements_ita_ptable_row:N \l_tmpa_clist 
							}
						\tex_cr:D
					}
				\bottomrule
			\endtabular
		\group_end:
		\end{center}
		\bigskip
	}

% #1 -> clist with elements
\cs_set:Nn \elements_ita_ptable_row:N
{
	\clist_gpop:NNT #1 \l_tmpa_tl
	{
		\tl_gset_eq:NN \g_tmpa_tl \l_tmpa_tl
		\elements_get_property_Z:Vn \g_tmpa_tl {symbol}
		\c_alignment_token
		\tl_use:N \g_tmpa_tl
		\c_alignment_token
		\elements_get_property_Z:Vn \g_tmpa_tl {mass}
	}
}

\cs_generate_variant:Nn \elements_get_property_Z:nn {Vn}

%============================================================%
%   ELEMENT BOXES
%============================================================%

\keys_define:nn { mendeleev/ptable }
	{
		property .tl_set:N  = \l_ptable_property_tl ,
		property .initial:n = mass,

		color .code:n    = { \color_set_eq:nn {ptable-color} {#1} } ,
		color .initial:n = black,

		size .dim_set:N = \l_ptable_box_size_dim,
		size .initial:n = 3.2em,

		scale .fp_set:N = \l_ptable_box_scale_fp,
		scale .initial:n = 1.0,

		line-width .dim_set:N = \l_ptable_line_width_dim,
		line-width .initial:n = 0.4pt,

		symbol-font .tl_set:N  = \l_ptable_symbol_font_tl,
		symbol-font .initial:n = \large\bfseries\sffamily,

		number-font .tl_set:N  = \l_ptable_number_font_tl,
		number-font .initial:n = \mdseries\scriptsize\sffamily,

		property-font .tl_set:N  = \l_ptable_property_font_tl,
		property-font .initial:n = \mdseries\scriptsize\sffamily,
	}

%============================================================%
%   PERIODIC TABLE ELEMENT
%============================================================%

\coffin_new:N \l_ptable_element_coffin

\cs_set:Nn \ptable_element:nn
{
	\color_group_begin:

	\dim_set:Nn \l_ptable_box_size_dim {3.2em}
	\IfNoValueF{#1}{ \keys_set:nn {mendeleev/ptable} {#1} }
	\color_select:n {ptable-color}	

	\ptable_element_coffin:n {#2}

	\coffin_typeset:Nnnnn \l_ptable_element_coffin {l}{vc}{0pt}{+1ex}

	\color_group_end:
}

\cs_set:Nn \ptable_element_coffin:n
{
	\hcoffin_set:Nn \l_ptable_element_coffin
	{
		\draw_begin:
			\draw_linewidth:n { \l_ptable_line_width_dim }
			\draw_path_rectangle:nn
			{ 0cm , 0cm }
			{ \l_ptable_box_size_dim , \l_ptable_box_size_dim }
			\draw_path_use_clear:n { stroke }
		\draw_end:
	}

	\ptable_box_attach:nnnnnnnn {#1} {symbol} {hc}{vc}{hc}{vc}{0pt}{+0.2ex}
	\ptable_box_attach:nnnnnnnn {#1} {number} {l}{t}{l}{t}{+0.6ex}{-0.6ex}
	\ptable_box_attach:nVnnnnnn {#1} \l_ptable_property_tl {hc}{b}{hc}{H}{0pt}{+0.6ex}

	\coffin_scale:NVV \l_ptable_element_coffin \l_ptable_box_scale_fp \l_ptable_box_scale_fp
}

\cs_generate_variant:Nn \coffin_scale:Nnn {NVV}

%% ATTACH PARAMETERS

\coffin_new:N \l__ptable_tmp_coffin

% #1 -> element
% #2 -> property
% #3, #4, #5, #6, #7, #8 -> coffin attach parameters
\cs_set:Nn \ptable_box_attach:nnnnnnnn
{
	\hcoffin_set:Nn \l__ptable_tmp_coffin
	{
		\tl_if_exist:cTF {l_ptable_#2_font_tl}
			{ \tl_use:c {l_ptable_#2_font_tl} }
			{ \tl_use:N \l_ptable_property_font_tl }

		\GetElementProperty {#1}{#2} 
	}
	\coffin_attach:NnnNnnnn \l_ptable_element_coffin {#3}{#4} \l__ptable_tmp_coffin {#5}{#6}{#7}{#8}
}

\cs_generate_variant:Nn \ptable_box_attach:nnnnnnnn {nVnnnnnn}

\NewDocumentCommand \PTableElement { o m }
{ \ptable_element:nn {#1}{#2} }

%============================================================%
%   PERIODIC TABLE ROW
%============================================================%

\keys_define:nn { mendeleev/ptable/row }
	{
		%% PTABLE ROW SORTING
		sort .bool_set:N = \l_ptable_row_sort_bool,
		sort .initial:n  = true,
	}

\coffin_new:N \l_ptable_row_coffin

% #1 -> ptable keys
% #2 -> clist with elements
\cs_set:Nn \ptable_row:nn
{	
	\color_group_begin:

	\clist_set:Nn \l_tmpa_clist {#2}

	\dim_set:Nn \l_ptable_box_size_dim {3.2em}
	\IfNoValueF{#1}{ \keys_set:nn {mendeleev/ptable} {#1} }
	\color_select:n {ptable-color}	

	\bool_if:NT \l_ptable_row_sort_bool
	{ \mendeleev_organize_elements:N \l_tmpa_clist  }

	\clist_map_inline:Nn \l_tmpa_clist
	{
		\ptable_element_coffin:n {##1}
	
		\coffin_join:NnnNnnnn \l_ptable_row_coffin {r}{H} \l_ptable_element_coffin {l}{H} {-\l_ptable_line_width_dim}{0pt}
	}
		
    \coffin_typeset:Nnnnn \l_ptable_row_coffin {l}{vc}{0pt}{+1ex}

	\color_group_end:
}
\cs_generate_variant:Nn \ptable_row:nn {nV}


\NewDocumentCommand \PTableRow
{ o m } { \ptable_row:nn {#1} {#2} }

\NewDocumentCommand \PTableRowExpand
{ o m } { \ptable_row:nx {#1} {#2} }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PROBLEMS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\keys_define:nn { braun/problems }
    {
        name .tl_set:N = \l_braun_problem_name_tl,
        name .initial:n = Problema,

        template .tl_set:N = \l_braun_problem_template_tl,
        template .initial:n = braun,

        skip-after .dim_set:N = \l_braun_problem_after_skip,
        skip-after .initial:n = 5pt,

        breakable .bool_set:N = \l_braun_problem_breakable_bool,
        breakable .initial:n  = false,
        breakable .default:n  = true,

        single-page .bool_set:N = \l_braun_problem_single_page_bool,
        single-page .initial:n  = false,
        single-page .default:n  = true,

		vfill .bool_set:N = \l_braun_problem_fill_bool,
        vfill .initial:n  = true,
        vfill .default:n  = true,
    }


\cs_set:Npn \path #1 { \seq_put_right:Nn \l_file_search_path_seq {#1} }

%============================================================%
%   CUSTOM LISTS FOR PROBLEMS
%============================================================%

\RequirePackage { tasks, enumitem, needspace }

\renewlist{itemize}{enumerate}{2}

\keys_define:nn { braun/lists }
    {
        enumerate .code:n = {
            \setlist [enumerate, 1] {#1}
        },
        enumerate .initial:n = {label = \textbf{\arabic*.}},

        itemize .code:n = {
            \setlist [itemize, 1] {#1}
        },
        itemize .initial:n = {label = \sffamily{\alph*.}, leftmargin=*},
    }

%%% CHOICES

\NewTasksEnvironment[
    label  = {\MiniBox{\Alph*}},
	%label  = {\textbf{\Alph*}\,(\;\;)},
    item-indent = 3em,
	%item-indent = 4em,
    after-item-skip = 2\itemsep,
    label-width = 1.5em,
	%label-width = 2.5em,
	label-align = right,
    label-offset = 0.7em,
]{choices}[\task]

%%% DATALIST

\NewTasksEnvironment[
	label = {$\bullet$},
	label-align = right,
]{datalist}[\item]

%%% ANSWERS

\newlist{answers}{enumerate}{2}
\setlist[answers,1]{label = \sffamily{\bfseries \arabic*.}}
\setlist[answers,2]{label = \sffamily{\alph*.}, leftmargin=*}

%%% OBJECTIVE ANSWERS

\NewTasksEnvironment[
	label = \sffamily{\small\textbf{\arabic*.}},
	label-align = right,
    item-indent = 3em,
    label-width = 1.5em,
    label-offset = 0.7em,
    before-skip = 1em,
]{checks}[\item]

%============================================================%
%   PROBLEM ENVIRONMENT
%============================================================%

\keys_define:nn { braun/problems }
    {
        id .tl_set:N = \l_braun_problem_id_tl,
        id .initial:n = ,

        path .tl_set:N = \g_braun_graphics_path_tl,
        path .initial:n = ,

        points .fp_set:N = \g_braun_graphics_points_fp,
        points .initial:n = 1.00,
    }

\box_new:N \l__braun_problem_box
\tl_new:N \l__braun_solution_tl

\cs_set:Nn \braun_begin_problem_box:
    { 
        \bool_if:NF \l_braun_problem_breakable_bool 
            { 
                \braun_ghost_section:
                \vbox_set:Nw \l__braun_problem_box 
            }
    }

\cs_set:Nn \braun_end_problem_box:
    { 
        \bool_if:NTF \l_braun_problem_breakable_bool 
            {
                \skip_vertical:N \l_braun_problem_after_skip
            }
            { 
                \vbox_set_end:
                \box_use_drop:N  \l__braun_problem_box
                \skip_vertical:N \l_braun_problem_after_skip
            }
		\bool_if:NT \l_braun_problem_fill_bool 
			{
				\skip_vertical:n {-2em} 
				\BraunVFill 
			}
    }

\newcounter { problem_counter } [ section ]
\newcounter { problem_counter_absolute }


% #1 -> set keys: braun/problem
\NewDocumentEnvironment { problem } { O{} }
    {
		\needspace{10\baselineskip}
        \refstepcounter{problem_counter}
		\refstepcounter{problem_counter_absolute}

        \keys_set:nn { braun/problems } {path = , id = , #1}

        \BraunNoWarning
        \dim_zero:N \parindent
        \braun_begin_problem_box:
        %% HEADER
        \str_case:VnF \l_braun_problem_template_tl
            {
                { braun }
                { 
                    \BraunHeader
                        [ \texttt{ \color{color-2} \l_braun_problem_id_tl } ]
                        { 
                            \small\sffamily\bfseries
                            \text_uppercase:n { \l_braun_problem_name_tl } ~
                            \arabic { section } . \arabic { problem_counter }
                        }
                }
                { IME }
                {
                    \skip_vertical:n {-1em}
                    \IMEHeader
                        [
                            \sffamily\bfseries
                            \skip_horizontal:n {2em}
                            Valor: ~  
                            \num 
                                [ 
                                    detect-all, 
                                    drop-zero-decimal=false, 
                                    round-mode=places, 
                                    round-precision=2,
                                ] 
                                { \fp_eval:n { \g_braun_graphics_points_fp } }
                            \skip_horizontal:n {2em}
                        ]
                        {
                            \sffamily\bfseries
                            \arabic { problem_counter }
                            \textsuperscript { a } ~
                            \text_uppercase:n { \l_braun_problem_name_tl }
                        }
                }       
            }
            {
                \paragraph{ \l_braun_problem_name_tl \; \arabic { problem_counter_absolute } }   
            }
    } 
    {
        \braun_end_problem_box:
        \bool_if:NT \l_braun_problem_single_page_bool { \newpage }
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   TEMPLATES
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\cs_set:Npn \DeclareBraunTemplate #1 #2
    { \keys_define:nn { braun } { #1 .meta:n = { #2 } } }

%============================================================%
%   ITA
%============================================================%

\DeclareBraunTemplate { ITA }
    {
        DIV = 20,
        font = lmodern,
        fontsize = 11pt,
        emph = \bfseries,
		page / section / name = ITA,
        maketitle / print = { title, subtitle, date },
        maketitle / title / case = upper,
        maketitle / title / font = \Large\bfseries,
		maketitle / subtitle /value = Turma~ IME-ITA,
        maketitle / subtitle / case = upper,
		maketitle / subtitle / font = \large\bfseries,
        maketitle / date / value = \int_use:N \c_sys_year_int,
        maketitle / date / font = \large\bfseries,
		maketitle / logo / value = ita-alt,
        maketitle / logo / value = pensi,
        problems / name = Questão,
        problems / template = ITA,
        graphics / width = \linewidth,
        graphics / height = 5cm,
    }


\DeclareBraunTemplate { ITAobj }
    {
        ITA,
		problems / breakable = true,
		problems / vfill = false,
    }


\DeclareBraunTemplate { ITAdis }
    {
        ITA,
		problems / breakable = false,
		problems / vfill = true,
    }

%============================================================%
%   IME
%============================================================%

\DeclareBraunTemplate { IME }
    {
        DIV = 16,
        font = helvetica,
        fontsize = 11pt,
        familydefault = sf,
        linewidth = 1.5pt,
        emph = \bfseries,
        page / IME,
        maketitle / align = c,
        maketitle / print = { title, subtitle, date },
        maketitle / toprule = false,
        maketitle / botrule = false,
        maketitle / title / case = upper,
        maketitle / title / font = \Large\bfseries,
        maketitle / subtitle /value = Turma~ IME-ITA,
        maketitle / subtitle / case = upper,
        maketitle / subtitle / font = \large\bfseries,
        maketitle / date / value = \int_use:N \c_sys_year_int,
        maketitle / date / font = \large\bfseries,
        maketitle / logo / value = ime,
        maketitle / logo / value = ita-alt,
        problems / name = Questão,
        problems / template = IME,
        graphics / width = \linewidth,
        graphics / height = 5cm,
        lists / itemize = {label = {\alph*)}},
		problems / breakable = true,
		problems / vfill = false,
    }

%============================================================%
%   IME
%============================================================%

\DeclareBraunTemplate { diagnostico }
    {
        DIV = 16,
        font = helvetica,
        fontsize = 11pt,
        familydefault = sf,
        linewidth = 1.5pt,
        emph = \bfseries,
        page / IME,
        maketitle / align = c,
        maketitle / print = { title, subtitle, date },
        maketitle / toprule = false,
        maketitle / botrule = false,
        maketitle / title / case = upper,
        maketitle / title / font = \Large\bfseries,
        maketitle / subtitle /value = Turma~ IME-ITA,
        maketitle / subtitle / case = upper,
        maketitle / subtitle / font = \large\bfseries,
        maketitle / date / value = \int_use:N \c_sys_year_int,
        maketitle / date / font = \large\bfseries,
        maketitle / logo / value = ime,
        maketitle / logo / value = pensi,
        problems / name = Questão,
        problems / template = IME,
        graphics / width = \linewidth,
        graphics / height = 5cm,
        lists / itemize = {label = {\alph*)}},
    }

%============================================================%
%   BRAUN
%============================================================%

\DeclareBraunTemplate { braun }
    {
        DIV = 23,
        font = paratype,
        fontsize = 9pt,
        emph = \itshape,
        page / headfoot-font = \sffamily ,
        page / footer / sepline = true,
        page / footer / title-sepline = true,
        page / footer / inner = { \textbf{\PrintTitle} \; | \; \PrintAuthor ,~ \PrintDate } ,
        page / footer / title-inner = { \textbf{\PrintTitle} \; | \; \PrintAuthor ,~ \PrintDate } ,
        page / footer / center = {},
        page / footer / title-center = {},
        page / footer / outer = \textbf{\thepage},
        page / footer / title-outer = \textbf{\thepage},
        page / mcrule / fancy,
        page / caption / labelfont = bf,
        page / caption / labelsep  = quad,
        page / caption / font      = sf,
        maketitle / pre-text = \thispagestyle { plain.scrheadings },
        maketitle / align = l,
        maketitle / print = { title, subtitle, author, affiliation },
        maketitle / toprule = true,
        maketitle / botrule = false,
        maketitle / title / font = \Huge\bfseries ,
        maketitle / subtitle / font = \Large\bfseries ,
        maketitle / author / font = \large\bfseries\sffamily ,
        maketitle / affiliation / font = \sffamily\slshape ,
        maketitle / date / value = \int_use:N \c_sys_year_int ,
        maketitle / date / font  = \Large\bfseries ,
        maketitle / logo / value = pensi,
        problems / name = Problema,
        problems / template = braun,
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
%   BEGIN DOCUMENT HOOK
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\AtBeginDocument
    {
        % PDF METADATA
		\RequirePackage { hyperref }
        \exp_args:Nx \hypersetup
            {
                pdftitle    = \text_purify:n { [\PrintAuthor]~\PrintTitle },
                pdfauthor   = \text_purify:n { \PrintAuthor   },
                pdfsubject  = \text_purify:n { \PrintSubtitle },
                pdfkeywords = Science,
                pdfproducer = Gabriel~Braun,
                pdfcreator  = Gabriel~Braun,
				hidelinks,
				breaklinks  = true,
				urlcolor    = color-1,
            }
        % KOMA SCRIPT
        \recalctypearea
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   DATABASE
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\clist_const:Nn \c_elements_clist
{
	H,	He,	Li,	Be,	B,	C,	N,	O,	F,	Ne,	Na,	Mg,	Al,	Si,	
    P,	S,	Cl,	Ar,	K,	Ca,	Sc,	Ti,	V,	Cr,	Mn,	Fe,	Co,	Ni,	
    Cu,	Zn,	Ga,	Ge,	As,	Se,	Br,	Kr,	Rb,	Sr,	Y,	Zr,	Nb,	Mo,	
    Tc,	Ru,	Rh,	Pd,	Ag,	Cd,	In,	Sn,	Sb,	Te,	I,	Xe,	Cs,	Ba,	
    La,	Ce,	Pr,	Nd,	Pm,	Sm,	Eu,	Gd,	Tb,	Dy,	Ho,	Er,	Tm,	Yb,	
    Lu,	Hf,	Ta,	W,	Re,	Os,	Ir,	Pt,	Au,	Hg,	Tl,	Pb,	Bi,	Po,	
    At,	Rn,	Fr,	Ra,	Ac,	Th,	Pa,	U,	Np,	Pu,	Am,	Cm,	Bk,	Cf,	
    Es,	Fm,	Md,	No,	Lr,	Rf,	Db,	Sg,	Bh,	Hs,	Mt
}

\prop_const_from_keyval:Nn \c_elements_H_prop
{
	number = 1, 
	symbol = H, 
	name = Hydrogen, 
	mass = 1.01, 
}

\prop_const_from_keyval:Nn \c_elements_He_prop
{
	number = 2, 
	symbol = He, 
	name = Helium, 
	mass = 4.00, 
}

\prop_const_from_keyval:Nn \c_elements_Li_prop
{
	number = 3, 
	symbol = Li, 
	name = Lithium, 
	mass = 6.94, 
}

\prop_const_from_keyval:Nn \c_elements_Be_prop
{
	number = 4, 
	symbol = Be, 
	name = Beryllium, 
	mass = 9.01, 
}

\prop_const_from_keyval:Nn \c_elements_B_prop
{
	number = 5, 
	symbol = B, 
	name = Boron, 
	mass = 10.81, 
}

\prop_const_from_keyval:Nn \c_elements_C_prop
{
	number = 6, 
	symbol = C, 
	name = Carbon, 
	mass = 12.01, 
}

\prop_const_from_keyval:Nn \c_elements_N_prop
{
	number = 7, 
	symbol = N, 
	name = Nitrogen, 
	mass = 14.01, 
}

\prop_const_from_keyval:Nn \c_elements_O_prop
{
	number = 8, 
	symbol = O, 
	name = Oxygen, 
	mass = 16.00, 
}

\prop_const_from_keyval:Nn \c_elements_F_prop
{
	number = 9, 
	symbol = F, 
	name = Fluorine, 
	mass = 19.00, 
}

\prop_const_from_keyval:Nn \c_elements_Ne_prop
{
	number = 10, 
	symbol = Ne, 
	name = Neon, 
	mass = 20.18, 
}

\prop_const_from_keyval:Nn \c_elements_Na_prop
{
	number = 11, 
	symbol = Na, 
	name = Sodium, 
	mass = 22.99, 
}

\prop_const_from_keyval:Nn \c_elements_Mg_prop
{
	number = 12, 
	symbol = Mg, 
	name = Magnesium, 
	mass = 24.31, 
}

\prop_const_from_keyval:Nn \c_elements_Al_prop
{
	number = 13, 
	symbol = Al, 
	name = Aluminium, 
	mass = 26.98, 
}

\prop_const_from_keyval:Nn \c_elements_Si_prop
{
	number = 14, 
	symbol = Si, 
	name = Silicon, 
	mass = 28.09, 
}

\prop_const_from_keyval:Nn \c_elements_P_prop
{
	number = 15, 
	symbol = P, 
	name = Phosphorus, 
	mass = 30.97, 
}

\prop_const_from_keyval:Nn \c_elements_S_prop
{
	number = 16, 
	symbol = S, 
	name = Sulfur, 
	mass = 32.06, 
}

\prop_const_from_keyval:Nn \c_elements_Cl_prop
{
	number = 17, 
	symbol = Cl, 
	name = Chlorine, 
	mass = 35.45, 
}

\prop_const_from_keyval:Nn \c_elements_Ar_prop
{
	number = 18, 
	symbol = Ar, 
	name = Argon, 
	mass = 39.95, 
}

\prop_const_from_keyval:Nn \c_elements_K_prop
{
	number = 19, 
	symbol = K, 
	name = Potassium, 
	mass = 39.10, 
}

\prop_const_from_keyval:Nn \c_elements_Ca_prop
{
	number = 20, 
	symbol = Ca, 
	name = Calcium, 
	mass = 40.08, 
}

\prop_const_from_keyval:Nn \c_elements_Sc_prop
{
	number = 21, 
	symbol = Sc, 
	name = Scandium, 
	mass = 44.96, 
}

\prop_const_from_keyval:Nn \c_elements_Ti_prop
{
	number = 22, 
	symbol = Ti, 
	name = Titanium, 
	mass = 47.87, 
}

\prop_const_from_keyval:Nn \c_elements_V_prop
{
	number = 23, 
	symbol = V, 
	name = Vanadium, 
	mass = 50.94, 
}

\prop_const_from_keyval:Nn \c_elements_Cr_prop
{
	number = 24, 
	symbol = Cr, 
	name = Chromium, 
	mass = 52.00, 
}

\prop_const_from_keyval:Nn \c_elements_Mn_prop
{
	number = 25, 
	symbol = Mn, 
	name = Manganese, 
	mass = 54.94, 
}

\prop_const_from_keyval:Nn \c_elements_Fe_prop
{
	number = 26, 
	symbol = Fe, 
	name = Iron, 
	mass = 55.84, 
}

\prop_const_from_keyval:Nn \c_elements_Co_prop
{
	number = 27, 
	symbol = Co, 
	name = Cobalt, 
	mass = 58.93, 
}

\prop_const_from_keyval:Nn \c_elements_Ni_prop
{
	number = 28, 
	symbol = Ni, 
	name = Nickel, 
	mass = 58.69, 
}

\prop_const_from_keyval:Nn \c_elements_Cu_prop
{
	number = 29, 
	symbol = Cu, 
	name = Copper, 
	mass = 63.55, 
}

\prop_const_from_keyval:Nn \c_elements_Zn_prop
{
	number = 30, 
	symbol = Zn, 
	name = Zinc, 
	mass = 65.38, 
}

\prop_const_from_keyval:Nn \c_elements_Ga_prop
{
	number = 31, 
	symbol = Ga, 
	name = Gallium, 
	mass = 69.72, 
}

\prop_const_from_keyval:Nn \c_elements_Ge_prop
{
	number = 32, 
	symbol = Ge, 
	name = Germanium, 
	mass = 72.63, 
}

\prop_const_from_keyval:Nn \c_elements_As_prop
{
	number = 33, 
	symbol = As, 
	name = Arsenic, 
	mass = 74.92, 
}

\prop_const_from_keyval:Nn \c_elements_Se_prop
{
	number = 34, 
	symbol = Se, 
	name = Selenium, 
	mass = 78.97, 
}

\prop_const_from_keyval:Nn \c_elements_Br_prop
{
	number = 35, 
	symbol = Br, 
	name = Bromine, 
	mass = 79.90, 
}

\prop_const_from_keyval:Nn \c_elements_Kr_prop
{
	number = 36, 
	symbol = Kr, 
	name = Krypton, 
	mass = 83.80, 
}

\prop_const_from_keyval:Nn \c_elements_Rb_prop
{
	number = 37, 
	symbol = Rb, 
	name = Rubidium, 
	mass = 85.47, 
}

\prop_const_from_keyval:Nn \c_elements_Sr_prop
{
	number = 38, 
	symbol = Sr, 
	name = Strontium, 
	mass = 87.62, 
}

\prop_const_from_keyval:Nn \c_elements_Y_prop
{
	number = 39, 
	symbol = Y, 
	name = Yttrium, 
	mass = 88.91, 
}

\prop_const_from_keyval:Nn \c_elements_Zr_prop
{
	number = 40, 
	symbol = Zr, 
	name = Zirconium, 
	mass = 91.22, 
}

\prop_const_from_keyval:Nn \c_elements_Nb_prop
{
	number = 41, 
	symbol = Nb, 
	name = Niobium, 
	mass = 92.91, 
}

\prop_const_from_keyval:Nn \c_elements_Mo_prop
{
	number = 42, 
	symbol = Mo, 
	name = Molybdenum, 
	mass = 95.95, 
}

\prop_const_from_keyval:Nn \c_elements_Tc_prop
{
	number = 43, 
	symbol = Tc, 
	name = Technetium, 
	mass = 97.91, 
}

\prop_const_from_keyval:Nn \c_elements_Ru_prop
{
	number = 44, 
	symbol = Ru, 
	name = Ruthenium, 
	mass = 101.07, 
}

\prop_const_from_keyval:Nn \c_elements_Rh_prop
{
	number = 45, 
	symbol = Rh, 
	name = Rhodium, 
	mass = 102.91, 
}

\prop_const_from_keyval:Nn \c_elements_Pd_prop
{
	number = 46, 
	symbol = Pd, 
	name = Palladium, 
	mass = 106.42, 
}

\prop_const_from_keyval:Nn \c_elements_Ag_prop
{
	number = 47, 
	symbol = Ag, 
	name = Silver, 
	mass = 107.87, 
}

\prop_const_from_keyval:Nn \c_elements_Cd_prop
{
	number = 48, 
	symbol = Cd, 
	name = Cadmium, 
	mass = 112.41, 
}

\prop_const_from_keyval:Nn \c_elements_In_prop
{
	number = 49, 
	symbol = In, 
	name = Indium, 
	mass = 114.82, 
}

\prop_const_from_keyval:Nn \c_elements_Sn_prop
{
	number = 50, 
	symbol = Sn, 
	name = Tin, 
	mass = 118.71, 
}

\prop_const_from_keyval:Nn \c_elements_Sb_prop
{
	number = 51, 
	symbol = Sb, 
	name = Antimony, 
	mass = 121.76, 
}

\prop_const_from_keyval:Nn \c_elements_Te_prop
{
	number = 52, 
	symbol = Te, 
	name = Tellurium, 
	mass = 127.60, 
}

\prop_const_from_keyval:Nn \c_elements_I_prop
{
	number = 53, 
	symbol = I, 
	name = Iodine, 
	mass = 126.90, 
}

\prop_const_from_keyval:Nn \c_elements_Xe_prop
{
	number = 54, 
	symbol = Xe, 
	name = Xenon, 
	mass = 131.29, 
}

\prop_const_from_keyval:Nn \c_elements_Cs_prop
{
	number = 55, 
	symbol = Cs, 
	name = Caesium, 
	mass = 132.91, 
}

\prop_const_from_keyval:Nn \c_elements_Ba_prop
{
	number = 56, 
	symbol = Ba, 
	name = Barium, 
	mass = 137.33, 
}

\prop_const_from_keyval:Nn \c_elements_La_prop
{
	number = 57, 
	symbol = La, 
	name = Lanthanum, 
	mass = 138.91, 
}

\prop_const_from_keyval:Nn \c_elements_Ce_prop
{
	number = 58, 
	symbol = Ce, 
	name = Cerium, 
	mass = 140.12, 
}

\prop_const_from_keyval:Nn \c_elements_Pr_prop
{
	number = 59, 
	symbol = Pr, 
	name = Praseodymium, 
	mass = 140.91, 
}

\prop_const_from_keyval:Nn \c_elements_Nd_prop
{
	number = 60, 
	symbol = Nd, 
	name = Neodymium, 
	mass = 144.24, 
}

\prop_const_from_keyval:Nn \c_elements_Pm_prop
{
	number = 61, 
	symbol = Pm, 
	name = Promethium, 
	mass = 144.91, 
}

\prop_const_from_keyval:Nn \c_elements_Sm_prop
{
	number = 62, 
	symbol = Sm, 
	name = Samarium, 
	mass = 150.36, 
}

\prop_const_from_keyval:Nn \c_elements_Eu_prop
{
	number = 63, 
	symbol = Eu, 
	name = Europium, 
	mass = 151.96, 
}

\prop_const_from_keyval:Nn \c_elements_Gd_prop
{
	number = 64, 
	symbol = Gd, 
	name = Gadolinium, 
	mass = 157.25, 
}

\prop_const_from_keyval:Nn \c_elements_Tb_prop
{
	number = 65, 
	symbol = Tb, 
	name = Terbium, 
	mass = 158.93, 
}

\prop_const_from_keyval:Nn \c_elements_Dy_prop
{
	number = 66, 
	symbol = Dy, 
	name = Dysprosium, 
	mass = 162.50, 
}

\prop_const_from_keyval:Nn \c_elements_Ho_prop
{
	number = 67, 
	symbol = Ho, 
	name = Holmium, 
	mass = 164.93, 
}

\prop_const_from_keyval:Nn \c_elements_Er_prop
{
	number = 68, 
	symbol = Er, 
	name = Erbium, 
	mass = 167.26, 
}

\prop_const_from_keyval:Nn \c_elements_Tm_prop
{
	number = 69, 
	symbol = Tm, 
	name = Thulium, 
	mass = 168.93, 
}

\prop_const_from_keyval:Nn \c_elements_Yb_prop
{
	number = 70, 
	symbol = Yb, 
	name = Ytterbium, 
	mass = 173.05, 
}

\prop_const_from_keyval:Nn \c_elements_Lu_prop
{
	number = 71, 
	symbol = Lu, 
	name = Lutetium, 
	mass = 174.97, 
}

\prop_const_from_keyval:Nn \c_elements_Hf_prop
{
	number = 72, 
	symbol = Hf, 
	name = Hafnium, 
	mass = 178.49, 
}

\prop_const_from_keyval:Nn \c_elements_Ta_prop
{
	number = 73, 
	symbol = Ta, 
	name = Tantalum, 
	mass = 180.95, 
}

\prop_const_from_keyval:Nn \c_elements_W_prop
{
	number = 74, 
	symbol = W, 
	name = Tungsten, 
	mass = 183.84, 
}

\prop_const_from_keyval:Nn \c_elements_Re_prop
{
	number = 75, 
	symbol = Re, 
	name = Rhenium, 
	mass = 186.21, 
}

\prop_const_from_keyval:Nn \c_elements_Os_prop
{
	number = 76, 
	symbol = Os, 
	name = Osmium, 
	mass = 190.23, 
}

\prop_const_from_keyval:Nn \c_elements_Ir_prop
{
	number = 77, 
	symbol = Ir, 
	name = Iridium, 
	mass = 192.22, 
}

\prop_const_from_keyval:Nn \c_elements_Pt_prop
{
	number = 78, 
	symbol = Pt, 
	name = Platinum, 
	mass = 195.08, 
}

\prop_const_from_keyval:Nn \c_elements_Au_prop
{
	number = 79, 
	symbol = Au, 
	name = Gold, 
	mass = 196.97, 
}

\prop_const_from_keyval:Nn \c_elements_Hg_prop
{
	number = 80, 
	symbol = Hg, 
	name = Mercury, 
	mass = 200.59, 
}

\prop_const_from_keyval:Nn \c_elements_Tl_prop
{
	number = 81, 
	symbol = Tl, 
	name = Thallium, 
	mass = 204.38, 
}

\prop_const_from_keyval:Nn \c_elements_Pb_prop
{
	number = 82, 
	symbol = Pb, 
	name = Lead, 
	mass = 207.20, 
}

\prop_const_from_keyval:Nn \c_elements_Bi_prop
{
	number = 83, 
	symbol = Bi, 
	name = Bismuth, 
	mass = 208.98, 
}

\prop_const_from_keyval:Nn \c_elements_Po_prop
{
	number = 84, 
	symbol = Po, 
	name = Polonium, 
	mass = 208.98, 
}

\prop_const_from_keyval:Nn \c_elements_At_prop
{
	number = 85, 
	symbol = At, 
	name = Astatine, 
	mass = 209.99, 
}

\prop_const_from_keyval:Nn \c_elements_Rn_prop
{
	number = 86, 
	symbol = Rn, 
	name = Radon, 
	mass = 222.02, 
}

\prop_const_from_keyval:Nn \c_elements_Fr_prop
{
	number = 87, 
	symbol = Fr, 
	name = Francium, 
	mass = 223.02, 
}

\prop_const_from_keyval:Nn \c_elements_Ra_prop
{
	number = 88, 
	symbol = Ra, 
	name = Radium, 
	mass = 226.03, 
}

\prop_const_from_keyval:Nn \c_elements_Ac_prop
{
	number = 89, 
	symbol = Ac, 
	name = Actinium, 
	mass = 227.03, 
}

\prop_const_from_keyval:Nn \c_elements_Th_prop
{
	number = 90, 
	symbol = Th, 
	name = Thorium, 
	mass = 232.04, 
}

\prop_const_from_keyval:Nn \c_elements_Pa_prop
{
	number = 91, 
	symbol = Pa, 
	name = Protactinium, 
	mass = 231.04, 
}

\prop_const_from_keyval:Nn \c_elements_U_prop
{
	number = 92, 
	symbol = U, 
	name = Uranium, 
	mass = 238.03, 
}

\prop_const_from_keyval:Nn \c_elements_Np_prop
{
	number = 93, 
	symbol = Np, 
	name = Neptunium, 
	mass = 237.05, 
}

\prop_const_from_keyval:Nn \c_elements_Pu_prop
{
	number = 94, 
	symbol = Pu, 
	name = Plutonium, 
	mass = 244.06, 
}

\prop_const_from_keyval:Nn \c_elements_Am_prop
{
	number = 95, 
	symbol = Am, 
	name = Americium, 
	mass = 243.06, 
}

\prop_const_from_keyval:Nn \c_elements_Cm_prop
{
	number = 96, 
	symbol = Cm, 
	name = Curium, 
	mass = 247.07, 
}

\prop_const_from_keyval:Nn \c_elements_Bk_prop
{
	number = 97, 
	symbol = Bk, 
	name = Berkelium, 
	mass = 247.07, 
}

\prop_const_from_keyval:Nn \c_elements_Cf_prop
{
	number = 98, 
	symbol = Cf, 
	name = Californium, 
	mass = 251.08, 
}

\prop_const_from_keyval:Nn \c_elements_Es_prop
{
	number = 99, 
	symbol = Es, 
	name = Einsteinium, 
	mass = 252.08, 
}

\prop_const_from_keyval:Nn \c_elements_Fm_prop
{
	number = 100, 
	symbol = Fm, 
	name = Fermium, 
	mass = 257.10, 
}

\prop_const_from_keyval:Nn \c_elements_Md_prop
{
	number = 101, 
	symbol = Md, 
	name = Mendelevium, 
	mass = 258.10, 
}

\prop_const_from_keyval:Nn \c_elements_No_prop
{
	number = 102, 
	symbol = No, 
	name = Nobelium, 
	mass = 259.10, 
}

\prop_const_from_keyval:Nn \c_elements_Lr_prop
{
	number = 103, 
	symbol = Lr, 
	name = Lawrencium, 
	mass = 262.11, 
}

\prop_const_from_keyval:Nn \c_elements_Rf_prop
{
	number = 104, 
	symbol = Rf, 
	name = Rutherfordium, 
	mass = 267.12, 
}

\prop_const_from_keyval:Nn \c_elements_Db_prop
{
	number = 105, 
	symbol = Db, 
	name = Dubnium, 
	mass = 268.13, 
}

\prop_const_from_keyval:Nn \c_elements_Sg_prop
{
	number = 106, 
	symbol = Sg, 
	name = Seaborgium, 
	mass = 271.13, 
}

\prop_const_from_keyval:Nn \c_elements_Bh_prop
{
	number = 107, 
	symbol = Bh, 
	name = Bohrium, 
	mass = 272.14, 
}

\prop_const_from_keyval:Nn \c_elements_Hs_prop
{
	number = 108, 
	symbol = Hs, 
	name = Hassium, 
	mass = 270.13, 
}

\prop_const_from_keyval:Nn \c_elements_Mt_prop
{
	number = 109, 
	symbol = Mt, 
	name = Meitnerium, 
	mass = 276.15, 
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ExplSyntaxOff