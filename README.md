# EasyReading

## Pitch
Know the difficulty level of your text with only one click.

## Description
EasyReading is a mobile app that classifies text based on its difficulty. It uses the European standard: A1, A2, B1, B2, C1 and C2, but simplified to only three levels: A, B or C.

The app allows the user to classify texts in Spanish. In future releases it will be able to recognize the language of the text and classify texts written in Spanish, Catalan and English. 

Target users of the app are people with reading, learning and/or other disabilities.

For text classification, the app uses Machine Learning (ML), which is a subfield of Artificial Intelligence. ML is used to create programs that are able to recognize patterns and/or classify texts using some previously-learned knowledge. 

In this case, it has analyzed some texts tagged with their difficulties. As a part of this analysis some metrics have been extracted from the texts and then used to train the program to classify new texts. Some of the extracted metrics are:
- words per sentence average
- letters per word average
- percentage of words of every grammatical category
- main verbs vs auxiliary verbs ratio

The app has only a few different screens which simplify its usage. The steps to be followed to classify text are:
1. Select some text from 1 of 3 possible sources
      - From a URL
      - From an attached file
      - From written text
2. Press “Process Text”
3. The App shows the user the difficulty level of the text

EasyReading was developed in the “PhoneGap” technology which allows it to be used in both Android or iOS devices.

## Installation

1. Download the repository on your local hard drive.
2. Install python 2.X and pip
3. Run the command "pip install requirements.txt"