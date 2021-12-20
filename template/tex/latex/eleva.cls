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
%          --  Eleva Template  -- 
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

\RequirePackage
    { 
        expl3,
        l3keys2e, 
        xparse,  
        silence,
    }
\ExplSyntaxOn

%============================================================%
%   FILTERED WARNINGS
%============================================================%

\WarningFilter{ hyperref }         { Token~not~allowed~in~a~PDF~string }
\WarningFilter{ blindtext }        { brazil~not~defined }
\WarningFilter{ typearea }         { Bad~type~area~settings! }
\WarningFilter{ latex }            { Font~shape }
\WarningFilter{ latex }            { Unused~global~option(s) }
\WarningFilter{ latex }            { \KOMAScriptVersion }
\WarningFilter{ scrlayer-scrpage } { \headheight }
\WarningFilter{ scrlayer-scrpage } { \footheight }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CLASS IDENTIFICATION                        
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\LoadClass [ twocolumn, twoside, fontsize=10pt ] { scrbook }

\ProvidesExplClass 
    { eleva } 
    { 2021/08/01 } 
    { 6.0 }
    { Apostila Eleva }

\RequirePackage [T1] { fontenc     }
\RequirePackage      { microtype   }
\RequirePackage      { scrhack     }
\RequirePackage      { anyfontsize }

\RequirePackage
    [ 
        top    = 3cm, 
        bottom = 3cm, 
        left   = 1.2cm, 
        right  = 1.2cm, 
        a4paper,
    ]
    { geometry }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   MACROS               
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% #1 -> module
% #2 -> keys
\NewDocumentCommand \braunsetup { o m } 
    { \exp_args:Ne \keys_set:nn { braun \IfValueT {#1} {/#1} } {#2} }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CLASS KEYS                   
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% The following options can only be set by \documentclass!
\keys_define:nn { braunclass }
    {
        %% DOCUMENT LANGUAGE
        language .code:n    = \PassOptionsToPackage {#1} { babel },
        language .initial:n = brazil,

        %% COLOR
        color .tl_set:N  = \l_braun_color_tl,
        color .initial:n = 00345A,
        
        %% UNKNOWN
        unknown .code:n = \exp_args:NV \KOMAoption \l_keys_key_tl {#1},
    }

\ProcessKeysOptions { braunclass }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PREAMBLE                 
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage
    { 
        babel,
        csquotes,
        float, 
        booktabs,
        scrlayer-scrpage,
        multicolrule,
        mathtools, 
        amssymb,
        siunitx,
        chemmacros,
        mendeleev,
    }

\numberwithin { equation     } { section }
\mathtoolsset { showonlyrefs }

\sisetup 
    { 
        range-phrase = { ~a~ }, 
        list-final-separator = { ~e~ }, 
        locale = FR,
    }

\chemsetup
    { 
        modules = { thermodynamics, nomenclature, isotopes, units, redox },
        formula = chemformula, 
        greek   = upgreek, 
    }

\sys_if_engine_pdftex:F { \selectchemgreekmapping { fontspec } }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BRAUN KEYS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\keys_define:nn { braun }
    {
        font .tl_set:N  = \g_braun_font_tl,

        familydefault .tl_set:N =  \g_braun_family_default_tl,

        emph .code:n = \cs_gset:Npn \emph ##1 { { #1 ##1 } },

        linewidth .dim_set:N  = \g_braun_linewidth_dim ,
        linewidth .initial:n  = 0.4pt,

        plot .code:n = 
            { \RequirePackage { pgfplots } \pgfplotsset { compat = 1.17 } },

        unknown .code:n = \exp_args:Ne \KOMAoption { \l_keys_key_tl } {#1},

        columnsep .dim_set:N = \columnsep,
        columnsep .initial:n = 3em,
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   COLORS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   FONT
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { mathptmx }
\RequirePackage [ scaled  ] { roboto }
\cs_gset_eq:NN \familydefault \sfdefault

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   SECTION HEADING
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\cs_generate_variant:Nn \color_select:nn {nV}

\addtokomafont { disposition } { \color { color-1 } }

\counterwithout { section } { chapter }

\KOMAoptions { numbers = endperiod }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BRAUNTEX
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { brauntitle, braunfig, braunbox, braunproblem, braunchem }

\braunsetup { problems/template = eleva, problems/breakable = true }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CHAPTER HEADING
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\tl_new:N \l_braun_chapter_image_tl

\cs_set:Npn  \chapterimage #1 { \tl_set:Nn \l_braun_chapter_image_tl {#1} }

\cs_gset:Npn \@makechapterhead #1
    {
        \group_begin:
        \dim_zero:N  \parindent
		\dim_gzero:N \@topnum % Prevents figures from going at top of page.
        \raggedright \normalfont
        \begin{tikzpicture} [ remember~picture, overlay ]
        \node at ( current~page.north~west )
            {
                \begin{tikzpicture} [ remember~picture, overlay ]
                    \node [ anchor = north~ west,inner~sep = 0pt ] at (0,0)  
                        {
                            \legacyincludegraphics
                                [ width = \paperwidth ]
                                { \l_braun_chapter_image_tl }
                        };
                    \draw [ fill = color-1, opacity=0.85 ] % aqui
                        ( 0cm, 0cm ) 
                        rectangle 
                        ( \paperwidth , -\paperwidth/5 );
                    \draw [ anchor = east ] 
                        ( \paperwidth - 1cm, -2.7  cm ) node 
                        [
                            circle,
                            line~width = 3pt,
                            align      = center,
                            draw       = color-1!50, % aqui
                            fill       = white,
                            inner~sep  = 1.2em,
                        ]
                        {
                            \group_begin:
                                \color { color-1 }
                                \sffamily
                                \fontsize { 12pt } { 12pt }
                                \textbf { ASSUNTO }
                            \group_end:
                            \\[1ex] 
                            \group_begin:
                                \color { color-1 }
                                \fontsize   { 60pt } { 60pt }
                                \fontseries {l} 
                                \selectfont
                                \thechapter
                            \group_end:
                        };
                    \draw [ draw = white, line~width = 3pt ] 
                        ( -2pt, -2cm ) -- ( 1.2cm, -2cm );
                    \draw [ anchor = west, align = left ] 
                        ( 1.5cm, -2cm ) node 
                        {
                            \group_begin:
                                \color { white }
                                \fontsize { 30pt } { 30pt } 
                                \selectfont
                                \textbf
                                    {
                                        \text_uppercase:n { \PrintSubtitle } 
                                    }
                            \group_end:
                            \\[1.2ex]
                            \group_begin:
                                \color { white }
                                \fontsize { 20pt } { 20pt } 
                                \selectfont
                                #1
                            \group_end:
                        };
                \end{tikzpicture}
            };
        \end{tikzpicture}
        \skip_vertical:n { \paperwidth/5 - 2cm }
        \group_end:
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   HEADER/FOOTER
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setkomafont { pageheadfoot } { \sffamily }

\ohead
    { 
        \group_begin:
            \Large
            \textbf { \text_uppercase:n { \PrintSubtitle } } 
        \group_end:
        \\[1ex] 
        \group_begin:
            Assunto~\thechapter 
        \group_end:
    }

\ihead  { \fontseries {l} \selectfont \large \leftmark }

\rofoot 
    [
        \textbf { \color { color-1 } \PrintTitle }   
        \quad
        { 
            \RoundBox 
                [ fill = color-1, yshift = 1.4em, stroke = color-1 ] 
                { \color { white } \textbf { \thepage } } 
        }
    ]
    { 
        \textbf { \color { color-1 } \PrintTitle } 
        \quad
        { 
            \RoundBox 
                [ fill = color-1, yshift = 1.4em, stroke = color-1 ] 
                { \color { white } \textbf { \thepage } } 
        }
    }
\lefoot 
    [
        { 
            \RoundBox 
                [ fill = color-1, yshift = 1.4em, stroke = color-1 ] 
                { \color { white } \textbf { \thepage } } 
        }
        \quad
        \textbf { \color { color-1 } \PrintTitle }    
    ]
    { 
        { 
            \RoundBox 
                [ fill = color-1, yshift = 1.4em, stroke = color-1 ] 
                { \color { white } \textbf { \thepage } } 
        }
        \quad
        \textbf { \color { color-1 } \PrintTitle } 
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   LISTS
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { enumitem }

\setlist [ enumerate, 1 ] { label={\arabic*}, wide, labelindent=0pt }

%============================================================%
%   ELEVA HEADER
%============================================================%

%% Header p/ outros
\DeclareBraunHeader { eleva }
	{
        \draw_path_rectangle:nn 
			{ 0cm  , 0cm }
			{ \linewidth, \coffin_ht:N \l__braun_txtb_coffin + 1.8em }
		\color_fill:n { color-1 }
        \draw_path_use_clear:n { fill }
        \draw_transform_shift:n 
			{ 2.5cm , 0.8em }
        \draw_coffin_use:Nnn \l__braun_txta_coffin {hc} {H}
	}

\cs_set:Npn \Level #1
	{
		\skip_vertical:n { 2ex }
		\ElevaHeader
			{ \Large \color{white} \bfseries Exercícios~ Nível~ #1  }
		\skip_vertical:n { 2ex }
	}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%