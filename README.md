[![Contributors][contributors-shield]](https://github.com/juju312000/DataEngineerProject/graphs/contributors)
[![LinkedIn_juju][linkedin-shield]](https://linkedin.com/in/jmarchadier)
[![LinkedIn_val][linkedin-shield]](https://linkedin.com/in/valentin-rebuffey-2b34aa22a)


<!-- PROJECT LOGO -->
<br />
<div align="center">
<h1 align="center">DataEngineerProject</h1>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#run project">Run project</a></li>
      </ul>
    </li>
    <li>
      <a href="#developer_guide">Developer_Guide</a></li>
      <ul>
        <li><a href="#data_cleaning">Data_Cleaning</a></li>
        <li>
          <a href="#dashboard">Dashboard</a>
            <ul>
              <li><a href="#frontend">Frontend</a></li>
              <li><a href="#backend">Backend</a></li>
            </ul>
        </li>
      </ul>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## Table of contents
* [Contact](#CONTACT) 

<!-- ABOUT THE PROJECT -->
## About The Project

This repository is a project of our second year of engineering study.
It took place in 1 month in DataEngineer course.

The goal is to create a web application based on Flask package.
This application should scrape data from website and print them (like with graphs).
Datas need to be stock on database seen in course.

So we decide to make an analysis of cryptocurrency and try to fit a model on daily values to predict tendency.
To build this, we use [CoinGecko website](https://www.coingecko.com) to collect data from the most used crypto-currencies.
We stock them on MongoDB client.
After collecting all the data, we start a Flask server who show 3 graphics :

* MarketCap : represent the total value of cryptocurrency in circulation. It can be obtain by multiply cryptocurrency value by the number of cryptocurrency.


* Volume : represent the number of cryptocurrency in circulation.


* Value : represent the cost of a cryptocurrency at one given time

The second page (when you clic on "predict") will show you a big graph where 70% first values represent the value of the cryptocurrency and on 30% last values there are :

* <u> Blue </u> : true values of cryptocurrency 


* <u> Green </u> : Predict values bases on SAMIRAX model (This model is the basic interface for ARIMA-type models, including those with exogenous regressors and those with seasonal components)
 

* <u> Yellow </u> : Predict values bases on AMIRA model (Seasonal AutoRegressive Integrated Moving Average)

To be deploy every where the application, we create a docker network with a docker compose to create 3 containers : MongoDB, PyScraping
and PyFlask.




<!-- CONTACT -->
## Contact

MARCHADIER Julien - julien.marchadier@edu.esiee.fr

Rebuffey Valentin - valentin.rebuffey@edu.esiee.fr

Project Link: [https://github.com/juju312000/DataEngineerProject](https://github.com/juju312000/DataEngineerProject )

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/juju312000/DataEngineerProject.svg?style=for-the-badge
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
