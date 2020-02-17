# dashapp

Airbnb is an amazing tool that allows citizens to advertise their houses, apartments, and rooms online for travelers to stay in.  In a city like New York City, there is so many tourists, that Airbnbs are very popular.  So I wanted to make a webapp using Dash/Plotly to help display some of the neighbourhoods that are the most expensive.  

The web app allows the user to specify which neighbourhood they want to look at.
* Brooklyn
* Queens
* Staten Island
* Manhattan
* Bronx

Once they select the neighbourhood, the graphs will slice and show the barplot with the sub-neighbourhoods and the sum of the prices.

![BarGraphs](https://user-images.githubusercontent.com/23482152/74620619-c16d2d00-5107-11ea-9240-7193e045d4ec.png)

We also wanted to look at how the number of reviews impacted the price on the apartment.  We can see that the price does have a minimum as shown by the distinct floor on the y axis.  But also we can see that as expected there is a high number of reviews on the lower end of the price spectrum.

![pricevreviews](https://user-images.githubusercontent.com/23482152/74620811-6d167d00-5108-11ea-8685-5790bf860614.png)

Some of the things that would need to be worked on is the performance.  Currently this app is only deployed on a development server.  So the next step would be to set up a production server to be able to deploy it if that was desired.


