
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#howtouse">How to use</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#dataset">Dataset</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
<div id="about-the-project"></div>

> An Exploratory Data Analysis of proposed Master thesis subjects

After the release of the proposed thesis subjects, I was curious, and I had so many questions:

- Most proposed subject (trending subject)
- Most prioritized specialty in our department
- Percentage of affected/unaffected subjects.
- Which teacher proposed different subjects. (the subjects he proposed where totally different)
- ... any many more.

So as a Data Scientist, I collected the data, Did some Exploratory Data Analysis and also 
created a __dashboard__ and deployed it so anyone interested is answering some of his question can interact
with it.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## How to use
<div id="howtouse"></div>

You can use the online version of the Dashboard located  [Here]()

To use it offline, follow the below steps:

### Prerequisites
<div id="prerequisites"></div>

You need to have:
- python 3.8
- pip3

### Installation
<div id="installation"></div>

<p align="right">(<a href="#top">back to top</a>)</p>


## Dataset Used
<div id="dataset"></div>


Each row in the dataset represents a proposed article from some teachers of 
Computer Science department (Faculty of Science/Ferhat Abbas Setif University) for 2022.

The data was collected by scraping some webpages found in the faculty website and saved as 
a csv file.

There is two version of the dataset:
1. original: this dataset contains only columns and data that was originally scraped for faculty website
2. modified: this dataset contains an additional column _Subject_ which was created manually,
this column contains one word that summarize the proposed thesis.

__Note__: the data contained in  _Subject_ column was created from my initial guesses after reading the
title of a proposed thesis, if you think there is a mistake, please open an issue
[open issues](https://github.com/khaledbouabdallah/Master_Subjects_Analysis/issues)
or contact me via linkdin.

___Dataset Columns___:
1. _ID_: 
2. _Title_:
3. _Author_:
4. _Grade_:
5. _Taken_:
6. _Priority 1_:
7. _Priority 2_:
8. _Priority 3_:
9. _Priority 4_:
10. _Priority 5_:
11. _Date_:
12. _Time_:
13. _Subject_:

Both datasets are available including the code used to scrap 
them and a clean version of the html files collected from the faculty website.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing
<div id="contributing"></div>

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License
<div id="license"></div>

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


## TODO
- say that you used:
  - streamlit
  - the readme dud
  - the streamlit guide 
- add instalation guide








