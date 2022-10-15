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

\tl_const:Nn \c_brauntex_base_class_tl { scrartcl }
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
\RequirePackage { microtype }

%============================================================%
%   KOMASCRIPT FEATURES
%============================================================%

\keys_define:nn { braun }
    { unknown .code:n  = \exp_args:NV \KOMAoption \l_keys_key_tl {#1} }

%============================================================%
%   FIGURES AND TABLES 
%============================================================%

\RequirePackage { float, booktabs, array }

%============================================================%
%   MATH
%============================================================%

\RequirePackage { mathtools, amssymb, textcomp, cancel }

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

\RequirePackage [ version = 4 ] { mhchem }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BOXES -> isso aqui vai morrer
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

\NewDocumentCommand \BraunHeader { O{} m }
    {
        \BraunNoWarning
        \skip_vertical:n { 1ex } 
        \group_begin:
            \dim_zero:N \parindent
            \draw_begin:
                \draw_linewidth:V \g_braun_linewidth_dim
                \hcoffin_set:Nn   \l__braun_txta_coffin {#2}
                \hcoffin_set:Nn   \l__braun_txtb_coffin {#1}
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
                \color_fill:n { gray-500 }
                \draw_path_use_clear:n { fill, stroke }
                \draw_transform_shift:n 
                    { \linewidth - 1em , 1.25ex }
                \draw_coffin_use:Nnn \l__braun_txtb_coffin {r}  {H}
                \draw_transform_shift:n 
                    { ( \coffin_wd:N \l__braun_txta_coffin + 4ex ) / 2 - \linewidth + 1em , 0cm }
                \draw_coffin_use:Nnn \l__braun_txta_coffin {hc} {H}
            \draw_end:
        \group_end:
        \skip_vertical:n { 1ex }
        \braun_ghost_section:
    }

%============================================================%
%   ChoiceBox
%============================================================%

% #1 -> content
% #2 -> size
\cs_set:Nn \braun_choice_box:nn
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
					\color_fill:n { gray-500 }
					\draw_path_use_clear:n { fill }
				\draw_end:
			}
		\hcoffin_set:Nn \l_tmpb_coffin {#1}
		\coffin_join:NnnNnnnn \l_tmpa_coffin {hc}{vc} \l_tmpb_coffin {hc}{vc} {0pt} {0pt}

		\coffin_typeset:Nnnnn \l_tmpa_coffin {\l_tmpb_coffin-H}{l} {0pt}{0pt}

		\group_end:
	}

%% FRONT-END

\cs_set:Npn \choicebox #1 
    { \braun_choice_box:nn  { \bfseries\sffamily\small #1 }{0.65em} }

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
    }

\tikzstyle{every~pin}=[draw=black]

%============================================================%
%   PALETA DE CORES (BOOTSTRAP)
%============================================================%

% CORES BÁSICAS
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

% TONS DE CINZA
\definecolor { gray-100 } { HTML } { f8f9fa }
\definecolor { gray-200 } { HTML } { e9ecef }
\definecolor { gray-300 } { HTML } { dee2e6 }
\definecolor { gray-400 } { HTML } { ced4da }
\definecolor { gray-500 } { HTML } { adb5bd } 
\definecolor { gray-600 } { HTML } { 6c757d } 
\definecolor { gray-700 } { HTML } { 495057 } 
\definecolor { gray-800 } { HTML } { 343a40 } 
\definecolor { gray-900 } { HTML } { 212529 } 
 
% CORES EM GRÁFICOS
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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CONFIGURAÇÕES DE PÁGINA
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { scrlayer-scrpage, multicolrule }

\pagestyle { scrheadings }

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
        columnsep .initial:n = 2em,
    }

%============================================================%
%   COLUMN SEPARATOR
%============================================================%

\keys_define:nn { braun/page/mcrule }
    { 
        fancy .meta:n = 
            {
                line-style = dashed,
                width      = thick,
                color      = gray-500,
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

\pagestyle { scrheadings }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   TÍTULO
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   ELEMENTOS DO TÍTULO
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

%% ELEMENTOS PADRÃO

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

%% LOGOS PREDEFINIDOS

\prop_const_from_keyval:Nn \l_braun_logos_prop
	{
		pensi = 
            {
                \draw_begin:  
                    \color_set:nnn {pensi}{HTML}{ffc107}
                    \fp_set:Nn \l_tmpa_fp { 60 } % Angle
                    \draw_path_moveto:n 
                        { 0em , 0em }
                    \draw_path_lineto:n 
                        { 0em , 1cm }
                    \draw_path_lineto:n 
                        { 1cm * ( sind(\l_tmpa_fp) ) / ( cosd(\l_tmpa_fp) + sind(\l_tmpa_fp) + 1 ) , 1cm }
                    \draw_path_arc:nnn { 90 } { - \l_tmpa_fp }
                        { 1cm * ( sind(\l_tmpa_fp) ) / ( cosd(\l_tmpa_fp) + sind(\l_tmpa_fp) + 1 ) }
                    \draw_path_close:   
                    \color_fill:n { white }
                    \draw_path_use:n { fill }
                    \draw_transform_shift:n 
                        {  
                            \draw_point_polar:nn 
                                { 0.7 * 1cm  } { 90 - \l_tmpa_fp / 2 }
                        }
                    \draw_path_moveto:n 
                        {
                            \draw_point_polar:nn 
                                {  1cm / ( 3 * sqrt(3) ) } { 0 }
                        }
                    \draw_path_lineto:n 
                        {
                            \draw_point_polar:nn
                                {  1cm / ( 3 * sqrt(3) ) } { 120 }
                        }
                    \draw_path_lineto:n 
                        {
                            \draw_point_polar:nn
                                {  1cm / ( 3 * sqrt(3) ) } { -120 }
                        }
                    \draw_path_close:
                    \color_fill:n { pensi!80 }
                    \draw_path_use:n { fill }
                \draw_end:
            },
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
			% \dim_zero:N  \parindent
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

            \thispagestyle { plain.scrheadings }

			\BraunSingleColumn
				{
                    \skip_vertical:n { -\headheight }
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
%   PROBLEMS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { tasks, enumitem }

%% RESPOSTAS DE PROBLEMAS OBJETIVOS

\NewTasksEnvironment
    [
        label = \sffamily{\small\textbf{\arabic*.}},
        label-align = right,
        item-indent = 3em,
        label-width = 1.5em,
        label-offset = 0.7em,
        before-skip = 1em,
    ]
    { checks } [ \item ]

%% ALTERNATIVAS DE PROBLEMAS OBJETIVOS

\NewTasksEnvironment
    [
        label  = {\choicebox{\Alph*}},
        item-indent = 3em,
        after-item-skip = 2\itemsep,
        label-width = 1.5em,
        label-align = right,
        label-offset = 0.7em,
    ] 
    { choices } [\item ]

%============================================================%
%   ALTERNATIVAS
%============================================================%

% Determinacão automática do número de colunas

\box_new:N \l_braun_choices_a_box
\box_new:N \l_braun_choices_b_box
\box_new:N \l_braun_choices_c_box
\box_new:N \l_braun_choices_d_box
\box_new:N \l_braun_choices_e_box

\fp_new:N \l_braun_choices_a_fp
\fp_new:N \l_braun_choices_b_fp
\fp_new:N \l_braun_choices_c_fp
\fp_new:N \l_braun_choices_d_fp
\fp_new:N \l_braun_choices_e_fp

% #1 -> alternativa A
% #2 -> alternativa B
% #3 -> alternativa C
% #4 -> alternativa D
% #5 -> alternativa E
\cs_set:Npn \autochoices #1#2#3#4#5
    {
        \group_begin:

        \hbox_set:Nn \l_braun_choices_a_box {#1}
        \hbox_set:Nn \l_braun_choices_b_box {#2}
        \hbox_set:Nn \l_braun_choices_c_box {#3}
        \hbox_set:Nn \l_braun_choices_d_box {#4}
        \hbox_set:Nn \l_braun_choices_e_box {#5}

        \fp_set:Nn \l_braun_choices_a_fp
            { \dim_to_decimal:n { \box_wd:N \l_braun_choices_a_box } }
        \fp_set:Nn \l_braun_choices_b_fp
            { \dim_to_decimal:n { \box_wd:N \l_braun_choices_b_box } }
        \fp_set:Nn \l_braun_choices_c_fp
            { \dim_to_decimal:n { \box_wd:N \l_braun_choices_c_box } }
        \fp_set:Nn \l_braun_choices_d_fp
            { \dim_to_decimal:n { \box_wd:N \l_braun_choices_d_box } }
        \fp_set:Nn \l_braun_choices_e_fp
            { \dim_to_decimal:n { \box_wd:N \l_braun_choices_e_box } }

        \fp_set:Nn \l_tmpa_fp 
            { % alternativa de maior tamanho
                max(
                    \l_braun_choices_a_fp,
                    \l_braun_choices_b_fp,
                    \l_braun_choices_c_fp,
                    \l_braun_choices_d_fp,
                    \l_braun_choices_e_fp
                )
            }
        \fp_set:Nn \l_tmpb_fp 
            { % tamanho útil
                0.8 * \dim_to_decimal:n {\columnwidth}
            }

        \int_set:Nn \l_tmpa_int 
            { % número de colunas
                \fp_to_int:n { min( 5, floor(\l_tmpb_fp  / \l_tmpa_fp) ) } 
            }

        \begin{choices}(\l_tmpa_int)
            \item #1
            \item #2
            \item #3
            \item #4
            \item #5
        \end{choices}

        \group_end:
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   FIGURAS E TABELAS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   INLCUSÃO DE IMAGENS
%============================================================%

\RequirePackage { svg }

\cs_set:Nn \graphics_include:n { \graphics_include:nn {} {#1} }

\keys_define:nn { braun/graphics }
	{
        % fps .code:n = { \cs_set_protected:Npn \fps@figure {#1} },
        % fps .initial:n = H,

        width .dim_set:N = \l_braun_graphics_width_dim,
		width .initial:n = 5cm,

		height .dim_set:N = \l_braun_graphics_height_dim,
		height .initial:n = 4cm,

        path .tl_set:N = \g_braun_graphics_path_tl,
        path .initial:n = {},
	}

\cs_set:Npn \path #1 
    { 
        \seq_put_right:Nn \l_file_search_path_seq {#1} 
        \tl_set:Nn \g_braun_graphics_path_tl {#1}
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

\tl_new:N \l_tmpc_tl

\cs_set_eq:NN \legacyincludegraphics \includegraphics

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
                        { \g_braun_graphics_path_tl \l_tmpa_tl / \l_tmpb_tl .tex }
                        { \braun_include_svg:Nn \l_tmpa_coffin {#2} }
                }      
            }
            {
                \braun_include_graphics:Nn \l_tmpa_coffin {#2}
            }

        \coffin_typeset:Nnnnn \l_tmpa_coffin {l} {vc} {0pt} {0pt}
        \group_end:
    }

%============================================================%
%   INCLUSÃO DE CONTEÚDO TABELADO
%============================================================%

% Compatibilidade com o PANDOC
\cs_set_eq:NN \tightlist    \relax
\cs_set_eq:NN \endhead      \relax
\cs_set_eq:NN \endfirsthead \relax

\tl_set:Nn \arraystretch {1.25}

\arrayrulecolor { gray-600 }

\NewDocumentEnvironment { longtable } { O{} m }
	{
        \group_begin:
        \begin{center}    
		\begin{tabular} [#1] {#2} 
		
	}
	{
		\end{tabular}
        \end{center}
		\group_end:
	}

%============================================================%
%   LEGENDAS
%============================================================%

\RequirePackage [ hypcap = false ] { caption }

\keys_define:nn { braun/caption }
    {
        font .code:n = \captionsetup { font = { #1 } },
        font .initial:n = {sf},

        labelformat .code:n = \captionsetup { labelformat = { #1 } },

        labelfont .code:n = \captionsetup { labelfont = { #1 } },
        labelfont .initial:n = {bf},

        labelsep .tl_set:N = \captionformat,
        labelsep .initial:n = \quad,

        unknown .code:n  = \exp_args:NV \captionsetup \l_keys_key_tl {#1}
    }

\DeclareCaptionLabelFormat { caps }
    {
        \text_uppercase:n {#1} ~ #2
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CAIXAS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { tcolorbox }

\tcbuselibrary { skins, breakable }

\tcbset { enhanced~ jigsaw }

%============================================================%
%   TABELA BONITINHA
%============================================================%

\keys_define:nn { braun/colortable }
    {
        caption-color .code:n = 
            \colorlet { colortable_caption_color } { #1 },
        caption-color .initial:n = blue!70!black,

        caption-label-color .code:n = 
            \colorlet { colortable_label_color } { #1 },
        caption-label-color .initial:n = red!80!black,

        frame-color .code:n = 
            \colorlet { colortable_frame_color } { #1 },
        frame-color .initial:n = orange,

        background-color .code:n = 
            \colorlet { colortable_background_color } { #1 },
        background-color .initial:n = yellow!7.5,
    }

\NewDocumentEnvironment { colortable } { O{} m +b }
    {
        \group_begin:

        \captionsetup
            {
                font = { sf, bf },
                labelformat = caps,
                labelfont = { color = colortable_label_color },
                textfont  = { color = colortable_caption_color },
            }

        \begin{table}
        \centering
        \tcbox
            [
                left = 0pt,
                right = 0pt,
                boxsep = 0pt,
                top = 2pt,
                bottom = -1.2em,
                toptitle = -0.8ex,
                bottomtitle = 1ex,
                lefttitle = 1ex,
                righttitle = 1ex,
                title =
                    { 
                        \captionof { table } { \boldmath \l_tmpa_tl } 
                    },
                colframe = colortable_frame_color,
                colback = white,
                colbacktitle = colortable_background_color,
                sharp~ corners = downhill,
                grow~ to~ left~ by = 1ex,
                arc = 1ex,
            ]
            {
                \cs_set_eq:NN \toprule    \relax
                \cs_set_eq:NN \bottomrule \relax
                \cs_set_eq:NN \caption    \relax

                \arrayrulecolor { colortable_frame_color }

                \dim_set:Nn \lightrulewidth {1pt}

                \begin{tabular} [#1] { @{\hspace{1ex}} #2 @{\hspace{1ex}} } 
                    #3
                \end{tabular}
            }
    } 
    {
        \end{table}
        \group_end:
    }

\NewDocumentEnvironment { displaytable } {}
	{
        \group_begin:

        \cs_set:Npn \paragraph ##1
            { \tl_set:Nn \l_tmpa_tl {##1} }

        \cs_set_eq:NN \longtable \colortable
        \cs_set_eq:NN \endlongtable \endcolortable
	}
	{
        \group_end:
	}

%============================================================%
%   EXEMPLOS
%============================================================%

\keys_define:nn { braun/examples }
    {
        color .code:n = 
            \colorlet { example_color } { #1 },
        color .initial:n = purple!60!black,

        background-color .code:n = 
            \colorlet { example_background_color } { #1 },
        background-color .initial:n = cyan!7.5,
    }

\newfloat  { floatexample } { thp } { loe }
\captionsetup [ floatexample ] { name = Exemplo }

\cs_set:Npn \ExampleHeader #1
    {
        \group_begin:

        \captionsetup
            {
                labelformat = caps,
                font = { color = example_color, sf },
                labelfont = bf,
            }

        \captionof{floatexample}{#1}  
        \skip_vertical:n {-1em}
 
        \group_end:  
    }

\newcounter { step } [ floatexample ]

\cs_set:Npn \ExampleSubHeader #1
    {
        \refstepcounter { step }

        \tcbsubtitle
            [
                enhanced, 
                frame~ hidden,
            ]
            {    
                {
                    \strut 
                    \bfseries
                    \color { example_color } 
                    \small
                    \sffamily 
                    Etapa~ \arabic{ step }. 
                }
                \; #1
            }
    }

\NewDocumentEnvironment { example } { }
    {
        \group_begin:

        \cs_set_eq:NN \subsubsection \ExampleHeader
        \cs_set_eq:NN \paragraph \ExampleSubHeader

        \bigskip

        \begin{tcolorbox}
            [
                breakable,
                parbox = false,
                colback = white,
                coltitle = black,
                colbacktitle = example_background_color,
                colframe = example_color,
                left = 1ex,
                right = 1ex,
                top = 1ex,
                bottom = 1ex,
                sharp~ corners = downhill,
                arc = 1ex,
            ]

        \dim_zero:N \parindent
        \dim_set_eq:NN \parskip \medskipamount
    } 
    {
        \end{tcolorbox}

        \bigskip

        \group_end:
    }

%============================================================%
%   PONTO PARA PENSAR
%============================================================%

\cs_set:Npn \ThinkHeader #1
    {
        \tcbsubtitle
            { 
                \usekomafont { disposition }
                \small
                \text_uppercase:n {#1}
            }
    }

\NewDocumentEnvironment { think } { }
    {
        \cs_set_eq:NN \subsubsection \ThinkHeader

        \medskip

        \begin{addmargin}{\parindent}
        \begin{tcolorbox}
            [
                hbox~ boxed~ title,
                frame~ hidden,
                sharp~ corners,
                top = -1pt,
                colback = white,
                coltitle = black,
                colbacktitle = white,
                fonttitle = \sffamily\bfseries,
                left = 0pt,
                right = 0pt,
                toptitle = 2pt,
                bottomtitle = 2pt,
                colframe = gray-500,
            ]
    } 
    {
        \end{tcolorbox}
        \end{addmargin}

        \medskip
    }

%============================================================%
%   INFO E ATENÇÃO
%============================================================%

\cs_set:Npn \InfoHeader #1
    {
        \tcbsubtitle
            [
                enhanced,
                frame~ hidden,
                coltext = black,
                colback = cyan!7.5,
            ]
            {

                \usekomafont { disposition }
                \text_uppercase:n {#1}
            }
    }


\NewDocumentEnvironment { info } { }
    {
        \group_begin:

        \cs_set_eq:NN \subsubsection \InfoHeader

        \bigskip

        \begin{tcolorbox}
            [
                sharp~ corners,
                frame~ hidden,
                colback = cyan!7.5,
                left = 1ex,
                right = 1ex,
                borderline~ vertical = {1.5pt}{0pt}{cyan!7.5},
                borderline~ horizontal = {1.5pt}{0pt}{cyan!70!black},
            ]
    } 
    {
        \end{tcolorbox}

        \bigskip

        \group_end:
    }

\cs_set:Npn \WarningHeader #1
    {
        \tcbsubtitle
            [
                enhanced,
                frame~ hidden,
                coltext = black,
                colback = yellow!7.5,
            ]
            {

                \usekomafont { disposition }
                \text_uppercase:n {#1}
            }
    }

\NewDocumentEnvironment { warning } { }
    {
        \group_begin:

        \cs_set_eq:NN \subsubsection \WarningHeader

        \bigskip

        \begin{tcolorbox}
            [
                sharp~ corners,
                frame~ hidden,
                colback = yellow!7.5,
                left = 1ex,
                right = 1ex,
                borderline~ vertical = {1.5pt}{0pt}{yellow!7.5},
                borderline~ horizontal = {1.5pt}{0pt}{yellow},
            ]
    } 
    {
        \end{tcolorbox}

        \bigskip

        \group_end:
    }

%============================================================%
%   PROVA (COMO ISSO É FEITO?)
%============================================================%

\cs_set:Npn \DerivationHeader #1
    {
        \tcbsubtitle
            [
                enhanced,
                frame~ hidden,
                coltext = black,
                colback = yellow!7.5,
            ]
            {

                \usekomafont { disposition }
                \text_uppercase:n {#1}
            }
    }


\NewDocumentEnvironment { derivation } { }
    {
        \group_begin:

        \cs_set_eq:NN \subsubsection \DerivationHeader

        \bigskip

        \begin{tcolorbox}
            [
                breakable,
                sharp~ corners,
                frame~ hidden,
                colback = yellow!7.5,
                left = 1ex,
                right = 1ex,
                borderline~ vertical = {1.5pt}{0pt}{yellow!7.5},
                borderline~ horizontal = {1.5pt}{0pt}{orange},
            ]
    } 
    {
        \end{tcolorbox}

        \bigskip

        \group_end:
    }

%============================================================%
%   RESUMO NO FINAL DA SEÇÃO
%============================================================%

\AtBeginEnvironment { quote }
    {
        \bfseries
        \itshape
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PROBLEMAS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   PROBLEMAS
%============================================================%

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

\cs_set:Nn \braun_ghost_section: { \subsection*{} \skip_vertical:n {-3em} }

\keys_define:nn { braun/problems }
    {
        id .tl_set:N = \l_braun_problem_id_tl,
        id .initial:n = ,

        path .tl_set:N = \g_braun_graphics_path_tl,
        path .initial:n = ,
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

\newcounter { problem } [ section ]

% #1 -> set keys: braun/problem
\NewDocumentEnvironment { problem } { O{} }
    {
        \refstepcounter{problem}

        \keys_set:nn { braun/problems } {path = , id = , #1}

        \bigskip
        %% HEADER
        \BraunHeader
            [ \texttt{ \color{pink} \l_braun_problem_id_tl } ]
            { 
                \footnotesize\sffamily\bfseries
                \text_uppercase:n { \l_braun_problem_name_tl } ~
                \arabic { section } . \arabic { problem }
            }

        \dim_zero:N \parindent
        \dim_set_eq:NN \parskip \medskipamount

        \skip_vertical:n { -1em } 
    } 
    {
        % \braun_end_problem_box:
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
%   BRAUN
%============================================================%

\DeclareBraunTemplate { braun }
    {
        DIV = 27,

        font = paratype,
        fontsize = 9pt,
        emph = \itshape,

        % Cabeçalhos
        headinclude = true,
        page / headfoot-font = \sffamily,
        page / header / sepline = true,
        page / header / inner = { \textbf{\PrintTitle} \; | \; \PrintAuthor ,~ \PrintDate },
        page / header / center = {},
        page / header / outer = \textbf{\thepage},

        % Rodapé
        footinclude = false,
        page / footer / inner = {},
        page / footer / center = {},
        page / footer / outer = {},

        % Rodapé da página de título
        page / footer / title-center = {},

        % Divisão das colunas (twocolumn)
        page / mcrule / fancy,

        % Título
        maketitle / align = l,
        maketitle / print = { title, subtitle, author, affiliation },
        maketitle / toprule = true,
        maketitle / botrule = true,
        maketitle / title / font = \Huge\bfseries ,
        maketitle / subtitle / font = \Large\bfseries ,
        maketitle / author / font = \large\bfseries\sffamily ,
        maketitle / affiliation / font = \sffamily\slshape ,
        maketitle / date / value = \int_use:N \c_sys_year_int ,
        maketitle / date / font  = \Large\bfseries ,
        maketitle / logo / value = pensi,

        % Legendas
        captions = nooneline,
        caption / labelfont = { color = blue!70!black, bf },
        caption / labelformat = caps,

        % Problemas
        problems / name = Problema,
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
%   PDF METADATA
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { hyperref }

\hypersetup
    {
        pdftitle    = { Braun },
        pdfauthor   = Gabriel~ Braun,
        pdfsubject  = Engenharia,
        pdfkeywords = {Ciência,~ Engenharia},
        pdfproducer = {Gabriel~ Braun},
        pdfcreator  = {Gabriel~ Braun},
        hidelinks,
        breaklinks  = true,
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\recalctypearea

\ExplSyntaxOff