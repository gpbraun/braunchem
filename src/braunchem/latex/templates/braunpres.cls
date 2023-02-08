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

\RequirePackage { l3keys2e, silence }

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
	{ braunpres }
	{ \c_brauntex_date_tl    }
	{ \c_brauntex_version_tl }
	{ \c_brauntex_info_tl    }

%============================================================%
%   BASE CLASS
%============================================================%

\tl_const:Nn \c_brauntex_base_class_tl { beamer }
\exp_args:NV \LoadClass \c_brauntex_base_class_tl

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BEAMER
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usetheme{metropolis}   

\cs_set:Npn\id#1{\relax}
\cs_set:Npn\affiliation#1{\relax}
\cs_set:Npn\path#1{\relax}

\cs_set_eq:NN \affiliation \institute

\cs_set:Npn\tightlist {\relax}

\cs_set_eq:NN \legacytableofcontents \tableofcontents

\cs_set:Npn \tableofcontents
	{
		\begin{frame}{Sumário}
			\legacytableofcontents%[hideallsubsections]
			\end{frame}
	}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BASIC 
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%============================================================%
%   MATH
%============================================================%

\RequirePackage { mathtools, amssymb, textcomp, cancel, marvosym }

\cs_set_eq:NN \degree \textdegree

%============================================================%
%   SI UNITS
%============================================================%

\RequirePackage { siunitx }

\sisetup 
  { 
    retain-explicit-plus,
    parse-units=false,
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
%   DRAWING
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { xcolor }
\RequirePackage { tikz }

\RequirePackage { braunchem }

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

%============================================================%
%   BIBLIOTECAS ADICIONAIS DO TIKZ/PGFPLOTS
%============================================================%

\AtBeginDocument 
  {
    \usepgfplotslibrary
      { 
        groupplots, 
        fillbetween 
      }
    \usetikzlibrary
      {
        calc,
        shapes.geometric, 
        decorations.pathreplacing,
        decorations.markings,
        decorations.pathmorphing,
        arrows.meta,
      }
  }

%============================================================%
%   PALETA DE CORES
%============================================================%

% CINZA
\definecolor { gray } { HTML } { 64748b }

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
\definecolor { lime   } { HTML } { 84cc16 }

% CORES DOS BLOCOS
\colorlet{ s-block } { blue   }
\colorlet{ p-block } { yellow }
\colorlet{ d-block } { red    }
\colorlet{ f-block } { purple }

% CORES EM GRÁFICOS
\pgfplotscreateplotcyclelist { braun-pallet }
  {
    { blue  },
    { red   },
    { green },
    { purple },
  }
\pgfplotsset
  {
    cycle~list~name = braun-pallet,
  }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ExplSyntaxOff
