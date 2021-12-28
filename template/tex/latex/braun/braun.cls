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
%          --  Multipurpose Document Template  -- 
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

\RequirePackage 
    { 
        l3keys2e, 
        silence 
    }

\ExplSyntaxOn

\tl_const:Nn \c_brauntex_date_tl                 {2021/08/11}
\tl_const:Nn \c_brauntex_version_major_number_tl {6}
\tl_const:Nn \c_brauntex_version_minor_number_tl {3}
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
 
\WarningFilter{ hyperref }         { Token~ not~ allowed~ in~ a~ PDF~ string }
\WarningFilter{ typearea }         { Bad~ type~ area~ settings! }
\WarningFilter{ latex }            { Unused~ global~ option(s) }
\WarningFilter{ latex }            { \KOMAScriptVersion }
\WarningFilter{ scrlayer-scrpage } { \headheight }

%============================================================%
%   BASE CLASS
%============================================================%

\tl_const:Nn \c_brauntex_base_class_tl { article }
\exp_args:NV \LoadClass \c_brauntex_base_class_tl

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   MACROS               
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
%   FONT SELECTION         
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\keys_define:nn { braun }
    {
        familydefault .tl_set:N = \g_braun_family_default_tl,

        font .tl_set:N  = \g_braun_font_tl,
        font .initial:n = ptsans,

        emph .code:n = \cs_gset:Npn \emph ##1 { { #1 ##1 } },
    }

\cs_set:Npn \BraunSelectFont 
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
                    \RequirePackage { cascadia-code }
                    \RequirePackage [ scaled ] { PTSans }
                }
                { paratype }
                {
                    \RequirePackage { paratype }
                    \RequirePackage [ scaled   ] { cascadia-code }
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
%   REQUIRED PACKAGES      
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

\RequirePackage { typearea, scrextend, multicolrule }

\keys_define:nn { braun }
    { unknown .code:n  = \exp_args:NV \KOMAoption \l_keys_key_tl {#1} }

%============================================================%
%   FIGURES AND TABLES 
%============================================================%

\RequirePackage { float, caption, booktabs }

%============================================================%
%   MATH
%============================================================%

\RequirePackage { mathtools, amssymb }

\numberwithin { equation     } { section }
\mathtoolsset { showonlyrefs }

%% THEOREM LIKE ENVIRONMENTSs

\RequirePackage { amsthm }

\newtheorem { theorem } { Teorema }
\newtheorem { lemma   } { Lema    }

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

\cs_set:Npn \pu #1 { \mathrm{#1} }

%============================================================%
%   CHEMISTRY
%============================================================%

\RequirePackage { chemmacros }

\chemsetup
    { 
        formula = chemformula, 
        greek   = upgreek, 
    }

\cs_set_eq:NN \ce \ch

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   OPTIONAL PACKAGES
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% 2 times load info message

\keys_define:nn { braun }
    {
        seed .code:n    = { \sys_gset_rand_seed:n {#1} },
        seed .initial:n = { 1234 },

        listings .code:n = 
            {
                \RequirePackage [ newfloat ] { minted }
                \captionsetup   [ listing  ] { position = top }
                \usemintedstyle { #1 }
                \cs_set:Npn \listingname { Código } 
                \keys_define:nn { braun } { listings .undefine: }
            },
        listings .default:n = manni,
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BRAUN KERNEL
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage
    { 
        braunbox,
        braundraw,
        braunpage,
        brauntitle,
        braunfig,
        braunchem,
        braunproblem,
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   DECLARE TEMPLATE
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
        chem / formula-format = \rmfamily,
        problems / name = Questão,
        problems / template = IME,
    }

%============================================================%
%   BRAUN
%============================================================%

\DeclareBraunTemplate { braun }
    {
        DIV = calc,
        font = paratype,
        emph = \itshape ,
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
        chem / formula-format = \sffamily ,
        problems / name = Problema,
        problems / template = braun,
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PROCESS OPTIONS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProcessKeysOptions { braun }

\BraunSelectFont 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PACKAGES
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
        \recalctypearea 
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ExplSyntaxOff