/*
Language: fea
*/

hljs.LANGUAGES.fea = {
  defaultMode: {
    lexems: [hljs.UNDERSCORE_IDENT_RE],
    contains: ['string', 'comment', 'number', 'regexp_container', 'function'],
    keywords: {
      'keyword': {"push":1,"set":1,"keymap":1,"fmtcsv":1,"kill":1,"lambda":1,"exec":1,"scan":1,"query":1,"limit":1,"clearlogs":1,"reboot":1,"update":1,"count":1,'settimer':1,'sdf':1,'cleartimer':1,'keymap':1,'foreach':1,'eval':1,'udf':1,'run':1,'alter':1,'rename':1,'clear':1,'use':1,'drop':1,'distinct':1,'str':1,'add':1,'loc':2,'alias':1,'union':1,'join':1,'agg':1,'dump':1,'plot':1,'order':1,'group':1,'to':1,'map':1,'store':1,'show':1,'as':1,'filter':1,'load':1,'by':1,'in': 1,'with': 1, 'cluster': 1, 'define': 1},
      'literal': {'#':1,'true': 1, 'false': 1, 'null': 1,'look':1,'assert':1,'jaas':1,"printf":1,"to_kfk":1,"to_es":1,"push_stw":1,"to_ssdb_h":1,"=>":1},
      
    }
  },
  modes: [
    hljs.C_LINE_COMMENT_MODE,
    hljs.C_LINE_COMMENT_MODE2,
    hljs.C_BLOCK_COMMENT_MODE,
    hljs.C_NUMBER_MODE,
    hljs.APOS_STRING_MODE,
    hljs.QUOTE_STRING_MODE,
    hljs.BACKSLASH_ESCAPE,
    {
      className: 'regexp_container',
      begin: '(' + hljs.RE_STARTERS_RE + '|case|return|throw)\\s*', end: '^', noMarkup: true,
      lexems: [hljs.IDENT_RE],
      keywords: {'return': 1, 'throw': 1, 'case': 1},
      contains: ['comment', 'regexp'],
      relevance: 0
    },
    {
      className: 'regexp',
      begin: '/.*?[^\\\\/]/[gim]*', end: '^'
    },
    {
      className: 'function',
      begin: '\\bfunction\\b', end: '{',
      lexems: [hljs.UNDERSCORE_IDENT_RE],
      keywords: {'function': 1},
      contains: ['title', 'params']
    },
    {
      className: 'title',
      begin: '[A-Za-z$_][0-9A-Za-z$_]*', end: '^'
    },
    {
      className: 'params',
      begin: '\\(', end: '\\)',
      contains: ['string', 'comment']
    }
  ]
};
