# draw.io automated AWS icon title insertion

I use draw.io a lot, and I discovered that it is convenient to have the many AWS icons not only visible by their logos, but also having the titles visible.

To avoid the manual insertion of all AWS icons, I have created a Python script that finds all AWS icons in a draw.io file which do not yet have a title, and it will insert the official title like e.g. "CloudFormation".

Prerequisite: 

* For the script to work, you need to make sure that draw.io is storing the diagrams in uncompressed XML files.
* To switch off compression in your draw.io desktop app, go to Extras > Configuration
* Then enter
```
{
  "compressXml": false
}
```
into the text box.
