# `pumla` Test Strategy

There are two kinds of tests that are done:
- automated tests as python scripts: With these the relevant functions of
  the pumla python command line tool are tested.
- the example diagrams in the test/examples folder: here overall tests are 
  performed, but they are manual. You have to check that all the example
  diagrams show the desired content when they render a diagram using PlantUML.
  This is hard to automate and typically also during work on the tool e.g.
  for new features or changes in the API, these examples need to change also.

So for each new feature that gets implemented:
- there should be an example diagram showing off the functionality of the feature
  under test/examples. If existing features are enhanced, also the enhancement
  of existing diagrams is ok. Maybe the existing diagrams do not even need to
  be changed, as the extended functionality automatically adds something to the
  diagram.
- if the new feature did include changes on the pumla command line tool, then the
  automated tests need to be executed and passed. If new functions are implemented
  in the context of the command line tool, add an automated test to test this function
  as a test case under test/test_cases and integrate it into the "test_all.py".
- perform a "pumla update" on the model repository in the test/examples folder.
  Then check all diagrams (not only the "new feature diagram) under test/examples
  that they still show the content that is
  intended when rendered with PlantUML, because the changes for the new feature
  might accidentally break some other feature. So check that also the other features
  are still working. If you are not sure anymore, what the intended content of a diagram
  is, compare it with the already rendered pictures stored in test/examples/pics.
  If the new feature leads to changed diagrams compared to the ones in test/examples/pics
  then save an updated version of the picture in the folder, if the content is ok.

The examples under test/examples are not only used for testing the different features, 
but also part of the pumla documentation. The examples are explained and referenced
from the Examples.md in the main folder. That way, these are not only feature tests, but
are re-used as examples for explaining how to use the different pumla features. So we
have a nice synergy here.
