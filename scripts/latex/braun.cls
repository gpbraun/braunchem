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

\RequirePackage { l3keys2e, l3draw, l3graphics }

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

\RequirePackage { typearea, scrextend, multicolrule }

\keys_define:nn { braun }
    { unknown .code:n  = \exp_args:NV \KOMAoption \l_keys_key_tl {#1} }

%============================================================%
%   FIGURES AND TABLES 
%============================================================%

\RequirePackage { float, booktabs }

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
%   BOXES
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\keys_define:nn { braun/box }
    {

        linewidth  .dim_set:N = \g_braun_linewidth_dim,
        linewidth  .initial:n = 0.4pt,

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
                legend~cell~align = left, 
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
        set~decimal~separator = {,},
    }

\pgfplotsset
    {
        compat = 1.17,
        samples = 150,
        no~markers,
        every~axis~plot/.append~style = {very~thick},   
    }
    
\tikzstyle{every pin}=[draw=black]

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

        linewidth .dim_set:N  = \g_braun_linewidth_dim ,
        linewidth .initial:n  = 0.4pt,

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

\cs_set:Nn \braun_ghost_section: { \legacysection*{} \skip_vertical:n {-3em} }

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
        }
        \group_end:
	}

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
		pensi = \file_input:n { pensi-logo.tex },
		ime   = \graphics_include:n { ime-logo.pdf },
		ita   = \graphics_include:n { ita-logo.pdf },
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

		linewidth .dim_set:N = \g_braun_linewidth_dim,
		linewidth .initial:n =  0.4pt,

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
		\cs_undefine:N \maketitle % save memory
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
		height .initial:n = 5cm,

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
        \file_if_exist:nT {#2}
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
        \str_case:Vn \l_tmpa_tl
            {
                { /uploads }
                {
                    \braun_include_graphics:Nn \l_tmpa_coffin {\l_tmpb_tl . \l_tmpc_tl}
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
    }


\cs_set:Npn \dbpath #1 { \seq_put_right:Nn \l_file_search_path_seq {#1} }

%============================================================%
%   CUSTOM LISTS FOR PROBLEMS
%============================================================%

\RequirePackage { tasks, enumitem }

%%% ENUMERATE (ITEMS)

\setlist[enumerate,1]{label = \sffamily{\bfseries \Roman*.}, leftmargin=*}
\setlist[enumerate,2]{label = \sffamily{(\roman*)}}

%%% ITEMIZE (TASKS)

\renewlist{itemize}{enumerate}{2}
\setlist[itemize,1]{label = \sffamily{\alph*.}, leftmargin=*}
\setlist[itemize,2]{label = \sffamily{(\roman*)}}

%%% CHOICES

\NewTasksEnvironment[
    label  = {\MiniBox{\Alph*}},
    item-indent = 3em,
    after-item-skip = 2\itemsep,
    label-width = 1.5em,
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
    item-indent = 2em,
    label-offset = 0.7em,
    before-skip = 1em,
]{checks}[\item]

%============================================================%
%   PROBLEM ENVIRONMENT
%============================================================%

\keys_define:nn { braun/problem }
    {
        id .tl_set:N = \l_braun_problem_id_tl,
        id .initial:n = ,

        path .tl_set:N = \g_braun_graphics_path_tl,
        path .initial:n = ,

        points .fp_set:N = \g_braun_graphics_points_fp,
        points .initial:n = 1.00,
    }

\counterwithout * { subsection } { section }

\box_new:N \l__braun_problem_box

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
                \BraunVFill
            }
    }

\newcounter { problem_counter } [ section ]

% #1 -> set keys: braun/problem
\NewDocumentEnvironment { problem } { O{} }
    {
        \refstepcounter{problem_counter}

        \keys_set:nn { braun/problem } {path = , id = , #1}

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
                \paragraph{ \l_braun_problem_name_tl ~ \arabic { problem_counter } }   
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
        chem / formula-format = \rmfamily,
        maketitle / print = { title },
        maketitle / title / case = upper,
        maketitle / title / font = \large\bfseries,
        problems / name = Questão,
        problems / template = ITA,
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
        maketitle / subtitle / case = upper,
        maketitle / subtitle / font = \Large\bfseries,
        maketitle / date / value = \int_use:N \c_sys_year_int,
        maketitle / date / font = \Large\bfseries,
        maketitle / logo / value = ime,
        maketitle / logo / value = pensi,
        problems / name = Questão,
        problems / template = IME,
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
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ExplSyntaxOff