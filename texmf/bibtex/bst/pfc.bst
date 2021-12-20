%%
%
% ARQUIVO: pfc.bst
%
% Formatação das referênicas de acordo com a NBR 6023:2002
% Baseado no arquivo plain.bst para uso com o pacote natbib (bibtex)
% VERSÃO: 1.0
% DATA: MAio de 2016
% AUTOR: Coordenação de Trabalhos Especiais SE/8
% 
% plain.bst
%  Copyright (C) 1984, 1985, 1988, 2010 Howard Trickey and Oren Patashnik.
%  Unlimited copying and redistribution of this file are permitted as long as
%  it is unmodified.  Modifications (and redistribution of modified versions)
%  are also permitted, but only if the resulting file is renamed to something
%  besides btxbst.doc, plain.bst, unsrt.bst, alpha.bst, and abbrv.bst.
%
%%

ENTRY
  { address
    author
    booktitle
    chapter
    edition
    editor
    howpublished
    institution
    isbn
    issn
    journal
    key
    month
    note
    number
    organization
    pages
    publisher
    school
    series
    title
    type
    url
    volume
    year
  }
  {}
  { label extra.label sort.label short.list }

INTEGERS { output.state before.all mid.sentence after.sentence after.block }

FUNCTION {bolden}
{ duplicate$ empty$
    { pop$ "" }
    { "{\bf " swap$ * "}" * }
  if$
}

FUNCTION {init.state.consts}
{ #0 'before.all :=
  #1 'mid.sentence :=
  #2 'after.sentence :=
  #3 'after.block :=
}

STRINGS { s t z e1 e2 }

FUNCTION {output.nonnull}
{ 's :=
  output.state mid.sentence =
    { ", " * write$ }
    { output.state after.block =
        { add.period$ write$
          newline$
          "\newblock " write$
        }
        { output.state before.all =
            'write$
            { add.period$ " " * write$ }
          if$
        }
      if$
      mid.sentence 'output.state :=
    }
  if$
  s
}


FUNCTION {output}
{ duplicate$ empty$
    'pop$
    'output.nonnull
  if$
}

FUNCTION {output.check}
{ 't :=
  duplicate$ empty$
    { pop$ "empty " t * " in " * cite$ * warning$ }
    'output.nonnull
  if$
}

FUNCTION {fin.entry}
{ add.period$
  write$
  newline$
}

FUNCTION {new.block}
{ output.state before.all =
    'skip$
    { after.block 'output.state := }
  if$
}

FUNCTION {new.sentence}
{ output.state after.block =
    'skip$
    { output.state before.all =
        'skip$
        { after.sentence 'output.state := }
      if$
    }
  if$
}

FUNCTION {not}
{   { #0 }
    { #1 }
  if$
}

FUNCTION {and}
{   'skip$
    { pop$ #0 }
  if$
}

FUNCTION {or}
{   { pop$ #1 }
    'skip$
  if$
}

FUNCTION {field.or.null}
{ duplicate$ empty$
    { pop$ "" }
    'skip$
  if$
}

FUNCTION {emphasize}
{ duplicate$ empty$
    { pop$ "" }
    { "{\em " swap$ * "}" * }
  if$
}

INTEGERS { nameptr namesleft numnames }

FUNCTION {capitalize}
{duplicate$ empty$
    { pop$ "" }
    { "{\MakeUppercase{" swap$ * "}}" * }
  if$
}


FUNCTION {scapify}
{ duplicate$ empty$
    { pop$ "" }
    { "{\sc " swap$ * "}" * }
  if$
}


FUNCTION {format.names}
{ 's :=
  #1 'nameptr :=
  s num.names$ 'numnames :=
  numnames 'namesleft :=
  { namesleft #0 > }
      { s nameptr "{vv~}{ll}{, jj}{, f.}" format.name$ capitalize 't :=
        nameptr #1 >
          { namesleft #1 >
%              { ", " * t * }
              { "; " * t * }
              { numnames #2 >
                  { " " * }
                  'skip$
                if$
                t "others" =
                  { " {\em et~al.}" * }
%                  { " e " * t * }
                  { "; " * t * }
                if$
              }
            if$
          }
          't
        if$
        nameptr #1 + 'nameptr :=
        namesleft #1 - 'namesleft :=
      }
  while$
}

FUNCTION {format.key}
{ empty$
    { key field.or.null }
    { "" }
  if$
}

FUNCTION {format.authors}
{ author empty$
    { "" }
    { author format.names }
  if$
}

FUNCTION {format.editors}
{ editor empty$
    { "" }
    { editor format.names scapify
      editor num.names$ #1 >
        { ", editores" * }
        { ", editor" * }
      if$
    }
  if$
}

FUNCTION {format.title}
{ title empty$
    { "" }
    { title "t" change.case$ }
  if$
}

FUNCTION {format.full.names}
{'s :=
  #1 'nameptr :=
  s num.names$ 'numnames :=
  numnames 'namesleft :=
    { namesleft #0 > }
    { s nameptr
      "{vv~}{ll}" format.name$ capitalize 't :=
      nameptr #1 >
        {
          namesleft #1 >
            { ", " * t * }
            {
              numnames #2 >
                { " " * }
                'skip$
              if$
              t "others" =
                { " et~al." * }
                { " e " * t * }
              if$
            }
          if$
        }
        't
      if$
      nameptr #1 + 'nameptr :=
      namesleft #1 - 'namesleft :=
    }
  while$
}

FUNCTION {author.editor.full}
{ author empty$
    { editor empty$
        { "" }
        { editor format.full.names }
      if$
    }
    { author format.full.names }
  if$
}

FUNCTION {author.full}
{ author empty$
    { "" }
    { author format.full.names }
  if$
}

FUNCTION {editor.full}
{ editor empty$
    { "" }
    { editor format.full.names }
  if$
}

FUNCTION {make.full.names}
{ type$ "book" =
  type$ "inbook" =
  or
    'author.editor.full
    { type$ "proceedings" =
        'editor.full
        'author.full
      if$
    }
  if$
}

FUNCTION {output.bibitem}
{ newline$
  "\bibitem[" write$
  label write$
  ")" make.full.names duplicate$ short.list =
     { pop$ }
     { * }
   if$
  "]{" * write$
  cite$ write$
  "}" write$
  newline$
  ""
  before.all 'output.state :=
}

FUNCTION {n.dashify}
{ 't :=
  ""
    { t empty$ not }
    { t #1 #1 substring$ "-" =
        { t #1 #2 substring$ "--" = not
            { "--" *
              t #2 global.max$ substring$ 't :=
            }
            {   { t #1 #1 substring$ "-" = }
                { "-" *
                  t #2 global.max$ substring$ 't :=
                }
              while$
            }
          if$
        }
        { t #1 #1 substring$ *
          t #2 global.max$ substring$ 't :=
        }
      if$
    }
  while$
}

FUNCTION {format.btitle}
{ title bolden 
}

FUNCTION {tie.or.space.connect}
{ duplicate$ text.length$ #3 <
    { "~" }
    { " " }
  if$
  swap$ * *
}

FUNCTION {either.or.check}
{ empty$
    'pop$
    { "can't use both " swap$ * " fields in " * cite$ * warning$ }
  if$
}

INTEGERS { multiresult }

FUNCTION {multi.page.check}
{ 't :=
  #0 'multiresult :=
    { multiresult not
      t empty$ not
      and
    }
    { t #1 #1 substring$
      duplicate$ "-" =
      swap$ duplicate$ "," =
      swap$ "+" =
      or or
        { #1 'multiresult := }
        { t #2 global.max$ substring$ 't := }
      if$
    }
  while$
  multiresult
}

FUNCTION {format.pages}
{ pages empty$
    { "" }
    { pages multi.page.check
        { "p{\'a}gs." pages n.dashify tie.or.space.connect }
        { "p{\'a}g." pages tie.or.space.connect }
      if$
    }
  if$
}

FUNCTION {format.msg.erro}
{ "ERRO (arquivo refs.bib): falta campo " 'e2 :=
  e2 e1 capitalize * 'e2 :=
  e2 " em @" * 'e2 :=
  e2 type$ capitalize * 'e2 :=
  e2 "\{" * 'e2 :=
  e2 cite$ capitalize * 'e2 :=
  "{\color{red}" * e2 * "}" * 
}

FUNCTION {format.article.items}
{ journal empty$
    { "journal" 'e1 :=
      ". " * format.msg.erro }
    { ". " * journal bolden * }
  if$
  volume empty$
    { "volume" 'e1 :=
      ", " * format.msg.erro }
    { ", v. " * volume *
      number empty$
        'skip$
        { ", n. " * number * }
      if$
    }
  if$
  pages empty$
    { url empty$
        { "pages ou url" 'e1 :=
          ". " * format.msg.erro }
        'skip$
      if$
    }
    { duplicate$ empty$
        { pop$ format.pages }
        { ", p. " * pages n.dashify * }
      if$
    }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  url empty$
    { "" * }
    { ". Disponível em: <" * url * ">" *}
  if$
  note empty$
    { url empty$ not
        { "note" 'e1 :=
          ". " * format.msg.erro }
        'skip$
      if$
    }
    { ". Acesso em: " * note * }
  if$
}

FUNCTION {format.book.items}
{ edition empty$
    { ". " * }
    { ". " * edition * ". ed. " * }
  if$
 address empty$ publisher empty$ and
    { "[S.l.: s.n.]" *}
    { address empty$
        { "[S.l.]: " * }
        { address * ": " * }
      if$
      publisher empty$
        { "[s.n.]" * }
        { publisher * }
      if$
    }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  pages empty$
    { "" * }
    { ". " * pages * " p" * }
  if$
  isbn empty$
    { "" * }
    { "ISBN " isbn * }
  if$
}

FUNCTION {format.inbook.items}
{ editor empty$
    { ". In: " * "\underline{\hspace{.5in}}. " * }
    { ". In: " * editor format.names * " (Org.). " *}
  if$
  booktitle empty$
    { "booktitle" 'e1 :=
      format.msg.erro }
    { booktitle bolden * }
  if$
  edition empty$
    { ". " * }
    { edition ". ed. " * }
  if$
  address empty$ publisher empty$ and
    { "[S.l.: s.n.]" *}
    { address empty$
        { "[S.l.]: " * }
        { address * ": " * }
      if$
      publisher empty$
        { "[s.n.]" * }
        { publisher * }
      if$
    }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  pages empty$
    { "" * }
    { ". p. " * pages n.dashify * }
  if$
  isbn empty$
    { "" * }
    { "ISBN " isbn * }
  if$
}

FUNCTION {format.inproceedings.items}
{ booktitle empty$
    { "booktitle" 'e1 :=
      ". In: " * format.msg.erro }
    { ". In: " * booktitle capitalize * }
  if$
  edition empty$
    { "edition" 'e1 :=
      ", " * format.msg.erro }
    { ", " * edition * "." * }
  if$
  series empty$
    { "" * }
    { ", " * series capitalize * }
  if$
  number empty$
    { series empty$ not
        { "number" 'e1 :=
          ", " * format.msg.erro 
          "." * }
        'skip$
      if$
    }
    { series empty$
        'skip$
        { ", " * number * "." *}
      if$
    }
  if$  
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  key empty$ not
    { ", " * key * }
    'skip$
  if$
  "Anais" 'z :=
  type "br" = url empty$ not and
    { "Anais eletrônicos" 'z := }
    'skip$
  if$
  type "intl" = url empty$ and
    { "Proceedings" 'z := }
    'skip$
  if$
  type "intl" = url empty$ not and
    { "Electronic proceedings" 'z := }
    'skip$
  if$
  ". " * z bolden * "... " * 
  address empty$ publisher empty$ and
    { "[S.l.: s.n.]" *}
    { address empty$
        { "[S.l.]: " * }
        { address * ": " * }
      if$
      publisher empty$
        { "[s.n.]" * }
        { publisher * }
      if$
    }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  pages empty$
    { url empty$
        { "pages ou url" 'e1 :=
          ". " * format.msg.erro }
        'skip$
      if$
    }
    { duplicate$ empty$
        { pop$ format.pages }
        { ", p. " * pages n.dashify * }
      if$
    }
  if$
  url empty$
    { "" * }
    { ". Disponível em: <" * url * ">" *}
  if$
  note empty$
    { url empty$ not
        { "note" 'e1 :=
          ". " * format.msg.erro }
        'skip$
      if$
    }
    { ". Acesso em: " * note * }
  if$
}

FUNCTION {format.techreport.items}
{ address empty$ publisher empty$ and
    { ". [S.l.: s.n.]" *}
    { address empty$
        { ". [S.l.]: " * }
        { ". " * address * ": " * }
      if$
      publisher empty$
        { "[s.n.]" * }
        { publisher * }
      if$
    }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  pages empty$
    { ". " * }
    { ". " * pages * " p. " * }
  if$
  number empty$
    { "(Relatório Técnico)" * }
    { "(Relatório Técnico, " * number * ")" * }
  if$
}

FUNCTION {format.siteurl.items}
{ url empty$
    { "url" 'e1 :=
      ". " * format.msg.erro }
    { ". Disponível em: <" * url * ">" *}
  if$
  note empty$
    { "note" 'e1 :=
      ". " * format.msg.erro }
    { ". Acesso em: " * note * }
  if$
}

FUNCTION {format.academic.items}
{ year empty$
    { "year" 'e1 :=
      format.msg.erro
      ". " * }
    { year * ". " * }
  if$
  pages empty$
    { "" * }
    { pages * " f. " * }
  if$
  z "tcc" =
    { "Trabalho de Conclusão de Curso " * }
    'skip$
  if$
  z "msc" =
    { "Dissertação " * }
    'skip$
  if$
  z "dsc" =
    { "Tese " * }
    'skip$
  if$
  series empty$
    { "series" 'e1 :=
      "(" * format.msg.erro
      ") " * }
    { "(" * series * ") " * }
  if$
  school empty$
    { "school" 'e1 :=
      "-- " * format.msg.erro }
    { "-- " * school * }
  if$
  address empty$
    { "address" 'e1 :=
      ", " * format.msg.erro }
    { ", " * address * }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  url empty$
    { "" * }
    { ". Disponível em: <" * url * ">" *}
  if$
  note empty$
    { url empty$ not
        { "note" 'e1 :=
          ". " * format.msg.erro }
        'skip$
      if$
    }
    { ". Acesso em: " * note * }
  if$
}

FUNCTION {format.event.key}
{ key empty$
    { "key" 'e1 :=
      ", " * format.msg.erro }
    { key capitalize * }
  if$
  series empty$
    { "series" 'e1 :=
      ", " * format.msg.erro }
    { " (" * series capitalize * ")" * }
  if$
}

FUNCTION {format.event.items}
{ edition empty$
    { "edition" 'e1 :=
      ", " * format.msg.erro }
    { ", " * edition * "." * }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  address empty$
    'skip$
    { ", " * address * }
  if$
  "Anais" 'z :=
  type "br" = url empty$ not and
    { "Anais eletrônicos" 'z := }
    'skip$
  if$
  type "intl" = url empty$ and
    { "Proceedings" 'z := }
    'skip$
  if$
  type "intl" = url empty$ not and
    { "Electronic proceedings" 'z := }
    'skip$
  if$
  ". " * z bolden * "... " * 
  address empty$ publisher empty$ and
    { "[S.l.: s.n.]" *}
    { address empty$
        { "[S.l.]: " * }
        { address * ": " * }
      if$
      publisher empty$
        { "[s.n.]" * }
        { publisher * }
      if$
    }
  if$
  year empty$
    { "year" 'e1 :=
      ", " * format.msg.erro }
    { ", " * year * }
  if$
  url empty$
    { note empty$ not
        { "url" 'e1 :=
          ". " * format.msg.erro }
        'skip$
      if$
    }
    { ". Disponível em: <" * url * ">" *}
  if$
  note empty$
    { url empty$ not
        { "note" 'e1 :=
          ". " * format.msg.erro }
        'skip$
      if$
    }
    { ". Acesso em: " * note * }
  if$
}



FUNCTION {article}
{ output.bibitem
  format.authors "author" output.check
  author format.key output
  new.block
  format.title "title" output.check
  new.block
  format.article.items "year" output.check
  new.block
  fin.entry
}

FUNCTION {book}
{ output.bibitem
  author empty$
    { format.editors "author and editor" output.check
      editor format.key output
    }
    { format.authors "author" output.check }
  if$
  new.block
  format.btitle "title" output.check
  new.block
  format.book.items "year" output.check
  new.block
  fin.entry
}

FUNCTION {inbook}
{ output.bibitem
  format.authors "author" output.check
  author format.key output
  new.block
  format.title "title" output.check
  new.block
  format.inbook.items "year" output.check
  new.block
  fin.entry
}

FUNCTION {inproceedings}
{ output.bibitem
  format.authors "author" output.check
  author format.key output
  new.block
  format.title "title" output.check
  new.block
  format.inproceedings.items "year" output.check
  new.block
  fin.entry
}

FUNCTION {techreport}
{ output.bibitem
  format.authors "author" output.check
  author format.key output
  new.block
  format.btitle "title" output.check
  new.block
  format.techreport.items "year" output.check
  new.block
  fin.entry
}

FUNCTION {siteurl}
{ output.bibitem
  author capitalize "author" output.check
  new.block
  title output.nonnull
  new.block
  format.siteurl.items "url" output.check
  new.block
  fin.entry
}

FUNCTION {academic}
{ output.bibitem
  format.authors "author" output.check
  author format.key output
  new.block
  title bolden output.nonnull ""
  new.block
  format.academic.items "year" output.check
  new.block
  fin.entry
}

FUNCTION {ugdthesis}
{ "tcc" 'z :=
  academic
}

FUNCTION {mscthesis}
{ "msc" 'z :=
  academic
}

FUNCTION {phdthesis}
{ "dsc" 'z :=
  academic
}

FUNCTION {event}
{ output.bibitem
%  key capitalize output.ckeck
  format.event.key output.ckeck
  new.block
  format.event.items "year" output.check
  new.block
  fin.entry
}


FUNCTION {default.type} { article }


READ

FUNCTION {sortify}
{ purify$
  "l" change.case$
}

INTEGERS { len }

FUNCTION {chop.word}
{ 's :=
  'len :=
  s #1 len substring$ =
    { s len #1 + global.max$ substring$ }
    's
  if$
}

FUNCTION {format.lab.names}
{ 's :=
  s #1 "{vv~}{ll}" format.name$
  s num.names$ duplicate$
  #2 >
    { pop$ " \NATetal{}" * }
    { #2 <
        'skip$
        { s #2 "{ff }{vv }{ll}{ jj}" format.name$ "others" =
            { " \NATetal{}" * }
            { "\NATand{} " * s #2 "{vv~}{ll}" format.name$ * }
          if$
        }
      if$
    }
  if$
}

FUNCTION {author.key.label}
{ author empty$
    { key empty$
        { cite$ #1 #3 substring$ }
         'series
      if$
    }
    { author format.lab.names }
  if$
}

FUNCTION {author.editor.key.label}
{ author empty$
    { editor empty$
        { key empty$
            { cite$ #1 #3 substring$ }
            'key
          if$
        }
        { editor format.lab.names }
      if$
    }
    { author format.lab.names }
  if$
}

FUNCTION {author.key.organization.label}
{ author empty$
    { key empty$
        { organization empty$
            { cite$ #1 #3 substring$ }
            { "The " #4 organization chop.word #3 text.prefix$ }
          if$
        }
        'key
      if$
    }
    { author format.lab.names }
  if$
}

FUNCTION {editor.key.organization.label}
{ editor empty$
    { key empty$
        { organization empty$
            { cite$ #1 #3 substring$ }
            { "The " #4 organization chop.word #3 text.prefix$ }
          if$
        }
        'key
      if$
    }
    { editor format.lab.names }
  if$
}

FUNCTION {calc.short.authors}
{ type$ "book" =
  type$ "inbook" =
  or
    'author.editor.key.label
    { type$ "proceedings" =
        'editor.key.organization.label
        { type$ "manual" =
            'author.key.organization.label
            'author.key.label
          if$
        }
      if$
    }
  if$
  'short.list :=
}


FUNCTION {calc.label}
{ calc.short.authors
  short.list
  "("
  *
  year duplicate$ empty$
  short.list key field.or.null = or
     { pop$ "" }
     'skip$
  if$
  *
  'label :=
}

FUNCTION {sort.format.names}
{ 's :=
  #1 'nameptr :=
  ""
  s num.names$ 'numnames :=
  numnames 'namesleft :=
    { namesleft #0 > }
    { nameptr #1 >
        { "   " * }
        'skip$
      if$
      s nameptr "{vv{ } }{ll{ }}{  ff{ }}{  jj{ }}" format.name$ 't :=
      nameptr numnames = t "others" = and
        { "et al" * }
        { t sortify * }
      if$
      nameptr #1 + 'nameptr :=
      namesleft #1 - 'namesleft :=
    }
  while$
}

FUNCTION {sort.format.title}
{ 't :=
  "A " #2
    "An " #3
      "The " #4 t chop.word
    chop.word
  chop.word
  sortify
  #1 global.max$ substring$
}

FUNCTION {author.sort}
{ author empty$
    { key empty$
        { "to sort, need author or key in " cite$ * warning$
          ""
        }
        { key sortify }
      if$
    }
    { author sort.format.names }
  if$
}

FUNCTION {author.editor.sort}
{ author empty$
    { editor empty$
        { key empty$
            { "to sort, need author, editor, or key in " cite$ * warning$
              ""
            }
            { key sortify }
          if$
        }
        { editor sort.format.names }
      if$
    }
    { author sort.format.names }
  if$
}

FUNCTION {author.organization.sort}
{ author empty$
    { organization empty$
        { key empty$
            { "to sort, need author, organization, or key in " cite$ * warning$
              ""
            }
            { key sortify }
          if$
        }
        { "The " #4 organization chop.word sortify }
      if$
    }
    { author sort.format.names }
  if$
}

FUNCTION {editor.organization.sort}
{ editor empty$
    { organization empty$
        { key empty$
            { "to sort, need editor, organization, or key in " cite$ * warning$
              ""
            }
            { key sortify }
          if$
        }
        { "The " #4 organization chop.word sortify }
      if$
    }
    { editor sort.format.names }
  if$
}

FUNCTION {presort}
{ calc.label
  label sortify
  "    "
  *
  type$ "book" =
  type$ "inbook" =
  or
    'author.editor.sort
    { type$ "proceedings" =
        'editor.organization.sort
        { type$ "manual" =
            'author.organization.sort
            'author.sort
          if$
        }
      if$
    }
  if$
  "    "
  *
  year field.or.null sortify
  *
  "    "
  *
  title field.or.null
  sort.format.title
  *
  #1 entry.max$ substring$
  'sort.label :=
  sort.label *
  #1 entry.max$ substring$
  'sort.key$ :=
}

ITERATE {presort}

SORT

STRINGS { longest.label last.label next.extra }

INTEGERS { longest.label.width last.extra.num number.label }

FUNCTION {initialize.longest.label}
{ "" 'longest.label :=
  #0 int.to.chr$ 'last.label :=
  "" 'next.extra :=
  #0 'longest.label.width :=
  #0 'last.extra.num :=
  #0 'number.label :=
}

FUNCTION {forward.pass}
{ last.label label =
    { last.extra.num #1 + 'last.extra.num :=
      last.extra.num int.to.chr$ 'extra.label :=
    }
    { "a" chr.to.int$ 'last.extra.num :=
      "" 'extra.label :=
      label 'last.label :=
    }
  if$
  number.label #1 + 'number.label :=
}

FUNCTION {reverse.pass}
{ next.extra "b" =
    { "a" 'extra.label := }
    'skip$
  if$
  extra.label 'next.extra :=
  extra.label
  duplicate$ empty$
    'skip$
    { "{\natexlab{" swap$ * "}}" * }
  if$
  'extra.label :=
  label extra.label * 'label :=
}

EXECUTE {initialize.longest.label}

ITERATE {forward.pass}

REVERSE {reverse.pass}

FUNCTION {bib.sort.order}
{ sort.label  'sort.key$ :=
}

ITERATE {bib.sort.order}

SORT

FUNCTION {begin.bib}
{ preamble$ empty$
    'skip$
    { preamble$ write$ newline$ }
  if$
  "\begin{thethesisbibliography}{" number.label int.to.str$ * "}" *
  write$ newline$
  "\expandafter\ifx\csname natexlab\endcsname\relax\def\natexlab#1{#1}\fi"
  write$ newline$
  "\expandafter\ifx\csname url\endcsname\relax" write$ newline$
  "  \def\url#1{{\tt #1}}\fi" write$ newline$
}

EXECUTE {begin.bib}

EXECUTE {init.state.consts}

ITERATE {call.type$}

FUNCTION {end.bib}
{ newline$
  "\end{thethesisbibliography}" write$ newline$
}

EXECUTE {end.bib}
