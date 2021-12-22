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
%          --  General Document Template  -- 
%
%============================================================%
%
%  GABRIEL P. BRAUN, 2019-2021
%
%============================================================
%
%  CONTACT: braun.pineschi@gmail.com
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage { l3keys2e }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CLASS IDENTIFICATION                        
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\PassOptionsToPackage{xcolor}{dvipsnames}

\LoadClass [tikz] {standalone}

\ProvidesExplClass{braundraw}{2021/08/01}{6.0}%
{ Braun Class }

\RequirePackage [T1] { fontenc }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   MACROS               
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% #1 -> module
% #2 -> keys
\NewDocumentCommand \braunsetup { o m } 
    { \exp_args:Ne \keys_set:nn { braun \IfValueT {#1} {/#1} } {#2} }

% #1 -> font name
% #2 -> family default
\cs_set:Nn \braun_use_font:nn
    {
        \RequirePackage { anyfontsize }
        %% FONT NAMES
        \str_case:nn {#1}
            {
                { lmodern }
                { 
                    \RequirePackage { lmodern  }
                }
                { ptsans }
                {
                    \RequirePackage { lmodern }
                    \RequirePackage [ scaled  ] { PTMono }
                    \RequirePackage [ scaled  ] { PTSans }
                }
                { paratype }
                {
                    \RequirePackage { paratype }
                    \RequirePackage { eulervm  }
                }
                { firasans }
                { 
                    \RequirePackage { lmodern }
                    \RequirePackage [ scaled  ] { FiraSans }
                }    
                { roboto }
                { 
                    \RequirePackage { lmodern }
                    \RequirePackage [ scaled  ] { roboto }
                }    
                { helvetica }
                { 
                    \RequirePackage { lmodern }
                    \RequirePackage [ scaled  ] { helvet }
                }          
            }
        % FAMILY DEFAULT
        \str_case:nn {#2}
            {
                { rm }
                { \cs_gset_eq:NN \familydefault \rmdefault }
                { sf }
                { \cs_gset_eq:NN \familydefault \sfdefault }
            }
    }
\cs_generate_variant:Nn \braun_use_font:nn {VV}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   TEMPLATES            
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% #1 -> template name
\cs_set:Nn \braun_use_template:n
    { 
        \file_input:n
            { templates / \str_lowercase:n{#1} . template .tex }
    }
\cs_generate_variant:Nn \braun_use_template:n {V}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   CLASS KEYS                   
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% The following options can only be set by \documentclass!
\keys_define:nn { braunclass }
    {
        %% BASIC DOCUMENT STYLE
        template .tl_set:N  = \g_braun_template_tl,
        template .initial:n = braun,

        %% SANS FONT
        familydefault .tl_set:N  =  \g_braun_family_default_tl,
        familydefault .initial:n = rm,

        %% DOCUMENT LANGUAGE
        language .code:n    = \PassOptionsToPackage {#1} { babel },
        language .initial:n = brazil,

        %% FONT CHOICES
        font .tl_set:N  = \g_braun_font_tl,
        font .initial:n = paratype,
        
        %% UNKNOWN
        unknown .code:n  = 
            \PassOptionsToClass { \l_keys_key_tl = #1 } { article },
    }

\ProcessKeysOptions { braunclass }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   PREAMBLE                 
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage
    { 
        csquotes,
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
        %% FONT CHOICES
        font .tl_set:N  = \g_braun_font_tl,

        %% SANS FONT
        familydefault .tl_set:N =  \g_braun_family_default_tl,

        %% EMPHASIS
        emph .code:n = \cs_gset:Npn \emph ##1 { { #1 ##1 } },

        %% DEFAULT LINEWIDTH
        linewidth .dim_set:N  = \g_braun_linewidth_dim ,
        linewidth .initial:n  = 0.4pt,

        %% LOAD PGFPLOTS
        plot .code:n = 
            { \RequirePackage { pgfplots } \pgfplotsset { compat = 1.17 } },
        plot .initial:n = true,

        %% UNKNOWN
        unknown .code:n = \exp_args:Ne \KOMAoption { \l_keys_key_tl } {#1},
    }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   BRAUN PACKAGES
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage
    { 
        brauncolor,
        %braunchem,
    }
    
\braun_use_font:VV \g_braun_font_tl \g_braun_family_default_tl

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                              
%   THE END!!!
%                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProcessKeysOptions { braun/colors }