## SafeLanguage
SafeLanguage has the goal to improve orthography in articles of the Spanish Wikipedia. Young people are a big part of readers of Wikipedia. By improving the quality of articles you can help to improve their use of the language. On the contrary, articles with misspellings of badly written could give young people the idea that language usage is a minor issue in communication.
### Goal
SafeLanguage aims to improve the global quality of articles in Spanish Wikipedia by improving the orthography of the articles. Although the read and improve one article at a time approach is probably the most effective way, a reviewer of an article has to deal with both: minor and major problems. In order to ease corrections over minor problems (like orthography) SafeLanguage could be run over an article before human intervention is needed.

For several years automatized tools -called bots- have been used to help improving the orthography of articles. However, these changes have to be reviewed one by one by a human. In particular, the bot called CEM-bot has over one million supervised corrections to the Spanish Wikipedia with less than 4% of wrong changes that has to be reverted by a human.

The goal of this project is to reduce the percentage of changes that a human has to revert after the execution of the bot.

### Actual steps in the execution of the bot
1. Download the last backup of the Spanish Wikipedia.

1. Transform it’s XML format into a grep’able format i.e one in which only content lines of articles are present, prepended by the name of the article.

1. Filter lines with “radicals”, i.e. lines in which one of the correction rules can be applied.

1. Filter to split paragraphs in sentences.

1. Correct selected articles with CEM-bot.

1. Manually check each of the changes made by the bot and revert any incorrect change.

Given that the number of articles with radicals is very high, steps 3 and 4 are normally applied over subsets of the rules given a slightly more complicated sequence of steps:

1. Download the last backup of the Spanish Wikipedia.

1. Transform it’s XML format into a grep’able format i.e one in which only content lines 
of articles are present, prepended.

1. Filter to split paragraphs in sentences.

1. Create an empty set of checked articles.

1. Create an empty set of applied rules.

1. While there are rules to be applied
   1. Select a subset of the non applied rules.
   1. Filter lines with radicals of the selected rules in non previously checked articles.
   1. Correct selected articles with CEM-bot.
   1. Include corrected files among the checked files (corrected files is a subset of the filtered files)
   1. Include selected rules among the applied rules.
   1. Manually check each of the changes made by the bot and revert any incorrect change.
   
### Problems with this approach
The selector uses a line by line approach and sometimes reasons for not correcting are outside of the scope of a line. For instance, a quote that spans over several lines (quotes are not corrected). The result is an article selected and not corrected.

* In a selected file, the bot introduces an error when changing a corrected word in Spanish (for instance, it  incorrectly changes trabajo into trabajó).

* In a selected file, the bot introduces an error when changing a corrected word in another language (for instance, it incorrectly changes poesia into poesía in a phrase written in Catalan).

### Proposed steps: First phase

1. Download the last backup of the Spanish Wikipedia.

1. Transform it’s XML format into a grep’able format i.e one in which only content lines of articles are present, prepended by the name of the article.

1. Filter to split paragraphs in sentences.

1. Filter lines with “radicals”, i.e. lines in which one of the correction rules can be applied.

1. Filter lines with the Spanish language selector.

1. Correct selected articles with CEM-bot.

1. Manually check each of the changes made by the bot and revert any incorrect change.

This sequence could reduce the corrections of phrases in other languages.

### Proposed steps: Second phase

1. Download the last backup of the Spanish Wikipedia.

1. Transform it’s XML format into a grep’able format i.e one in which only content lines of articles are present, prepended by the name of the article.

1. Filter to split paragraphs in sentences.

1. Filter lines with “radicals”, i.e. lines in which one of the correction rules can be applied.

1. Filter radicals with the Spanish language selector.

1. Filter out radical over correct phrases.

1. Correct selected articles with CEM-bot.

1. Manually check each of the changes made by the bot and revert any incorrect change.

This sequence could additionally reduce the introduction of errors in correct phrases.

## Meassure of impact

The impact of the project can be meassured comparing the number of reverts once uno or both filters are applied.


