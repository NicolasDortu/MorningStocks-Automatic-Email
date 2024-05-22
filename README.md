# MorningStocks-Automatic-Email
This script aims to send a daily update of an investment portfolio containing a table with : </br>

<ul>
  <li>The daily variation in % (from yesterday open and closure prices)</li>
  <li>PER (for stocks)</li>
  <li>Most Recent Earning (for stocks)</li>
  <li>Next Future Earning (for stocks)</li>
  <li>A chart of past 30 days performance</li>
  <li>Some related news from the NewsAPI services (https://newsapi.org/)</li>
</ul>

It heavily relies on the libraries Yfinance (https://github.com/ranaroussi/yfinance) and Yagmail (https://github.com/kootenpv/yagmail) to gather the tickers data and send the mail in an HTML format. </br>

The project is heavily inspired by Sven-Bo's python morning mailer bot (https://github.com/Sven-Bo/python-morning-mailer-bot). Shout-out to him ! 🙌 </br>

In order to send the mail, PythonAnywhere scheduled tasks perfectly do the job (https://www.pythonanywhere.com/) </br>

Don't forget to create a .env file with the following information : </br>

EMAIL_SENDER=YourGmailAdress</br>
EMAIL_PASSWORD=YourGmailPassword</br>
EMAIL_RECEIVER=YourEmailAdress</br>
NEWS_API_ORG_KEY=YourNewsAPIKey</br>


Here is an example of the result (22/05/24) : 
<html>
   <body style="margin: 0; padding: 0;">
      <table border="1" style="border-collapse: collapse; width: 100%; table-layout: fixed;">
         <thead>
            <tr>
               <th style="padding: 4px;">Ticker</th>
               <th style="padding: 4px;">Variation (%)</th>
               <th style="padding: 4px;">PER</th>
               <th style="padding: 4px;">Most Recent Earning</th>
               <th style="padding: 4px;">Next Future Earning</th>
               <th style="padding: 4px;">Chart (30 days period)</th>
            </tr>
         </thead>
         <tbody>
            <tr>
               <th colspan="6" style="padding: 8px; text-align:center; font-size: 1.2em;"><strong>Stocks - Unweighted Average Variation: 0.59%</strong></th>
            </tr>
            <tr>
               <th style="text-align:center; padding: 4px;"><strong>Apple</strong></th>
               <th style="text-align:center; padding: 4px;">0.66</th>
               <th style="text-align:center; padding: 4px;">29.935032</th>
               <th style="text-align:center; padding: 4px;">Date: 2024-05-02<br/>EPS Estimate: 1.5<br/>Reported EPS: 1.53</th>
               <th style="text-align:center; padding: 4px;">Date: 2024-08-01<br/>EPS Estimate: 1.32<br/>Reported EPS: nan</th>
               <th style="text-align:center; padding: 4px;"><img alt="Apple chart" src="https://github.com/NicolasDortu/MorningStocks-Automatic-Email/assets/126513916/e8825d97-6975-474d-ab46-204e46dacffb"/></th>
            </tr>
            <tr>
               <td colspan="6" style="text-align:left; padding: 4px;"><strong>News:</strong> <a href="https://gizmodo.com/samsung-apple-crush-commercial-1851481989">Samsung Disses Apple Over iPad Commercial Fiasco</a><br/>Every now and then a corporation is at least a bit funny when going about their late-stage capitalism. For instance, Samsung has released an absolutely perfect diss-ad response to Apple’s recent crushing PR disaster.Read more...</th>
            </tr>
            <tr>
               <th style="text-align:center; padding: 4px;"><strong>Microsoft</strong></th>
               <th style="text-align:center; padding: 4px;">0.52</th>
               <th style="text-align:center; padding: 4px;">37.364384</th>
               <th style="text-align:center; padding: 4px;">Date: 2024-05-21<br/>EPS Estimate: 2.82<br/>Reported EPS: 2.94</th>
               <th style="text-align:center; padding: 4px;">Date: 2024-05-29<br/>EPS Estimate: nan<br/>Reported EPS: nan</th>
               <th style="text-align:center; padding: 4px;"><img alt="Microsoft chart" src="https://github.com/NicolasDortu/MorningStocks-Automatic-Email/assets/126513916/cff77fc4-714e-4791-bc4b-f6f2b0ee45a7"/></th>
            </tr>
            <tr>
               <td colspan="6" style="text-align:left; padding: 4px;"><strong>News:</strong> <a href="https://www.theverge.com/2024/5/20/24160451/microsoft-surface-event-what-to-expect-ai">What to expect from Microsoft’s Surface event today</a><br/>Microsoft is holding a press-only event to discuss its AI and Surface device plans on May 20th, ahead of its Microsoft Build 2024 conference.</th>
            </tr>
            <tr>
               <th colspan="6" style="padding: 8px; text-align:center; font-size: 1.2em;"><strong>ETFs - Unweighted Average Variation: 0.08%</strong></th>
            </tr>
            <tr>
               <th style="text-align:center; padding: 4px;"><strong>MSCI World</strong></th>
               <th style="text-align:center; padding: 4px;">0.06</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;"><img alt="MSCI World chart" src="https://github.com/NicolasDortu/MorningStocks-Automatic-Email/assets/126513916/9911ab4f-b23d-4ba2-9759-8c2bb04d36ac"/></th>
            </tr>
            <tr>
               <td colspan="6" style="text-align:left; padding: 4px;"><strong>News:</strong> <a href="https://biztoc.com/x/b817ef39c9c08d8b">MicroStrategy Secures Spot on Prestigious MSCI World Stock Index</a><br/>MicroStrategy, the business intelligence and software firm well known for its substantial bitcoin holdings, has achieved a significant milestone by being added to the prestigious MSCI World Stock Index. The MSCI World Stock Index is a widely recognized benchm…</th>
            </tr>
            <tr>
               <th style="text-align:center; padding: 4px;"><strong>S&amp;P 500</strong></th>
               <th style="text-align:center; padding: 4px;">0.10</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;"><img alt="S&amp;P 500 chart" src="https://github.com/NicolasDortu/MorningStocks-Automatic-Email/assets/126513916/d30fb6d8-7031-4781-a185-dd469e9a76cd"/></th>
            </tr>
            <tr>
               <td colspan="6" style="text-align:left; padding: 4px;"><strong>News:</strong> <a href="https://finance.yahoo.com/video/catalysts-could-push-p-500-145656140.html">These catalysts could push the S&amp;P 500 to 5,600: BMO's Belski</a><br/>BMO Capital Markets recently increased its target for the S&amp;P 500 (^GSPC) to 5600, the highest forecast on Wall Street. The Dow Jones Industrial (^DJI...</th>
            </tr>
            <tr>
               <th colspan="6" style="padding: 8px; text-align:center; font-size: 1.2em;"><strong>Currencies - Unweighted Average Variation: 0.00%</strong></th>
            </tr>
            <tr>
               <th style="text-align:center; padding: 4px;"><strong>EUR/USD</strong></th>
               <th style="text-align:center; padding: 4px;">0.00</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;"><img alt="EUR/USD chart" src="https://github.com/NicolasDortu/MorningStocks-Automatic-Email/assets/126513916/3f17ec0c-00a0-4c13-9f30-afd3ff1a107d"/></th>
            </tr>
            <tr>
               <td colspan="6" style="text-align:left; padding: 4px;"><strong>News:</strong> <a href="https://biztoc.com/x/ac932c59c4f6dc69">EUR-USD Forecast: A Potential Long-Term Headache</a><br/>The EUR-USD pair, trading at $1.0872, is like a bad relationship – it’s complicated. Depending on your time frame, it’s either a promising fling or... #eurusd</th>
            </tr>
            <tr>
               <th colspan="6" style="padding: 8px; text-align:center; font-size: 1.2em;"><strong>Commodities - Unweighted Average Variation: -0.32%</strong></th>
            </tr>
            <tr>
               <th style="text-align:center; padding: 4px;"><strong>Gold</strong></th>
               <th style="text-align:center; padding: 4px;">-0.32</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;"><img alt="Gold chart" src="https://github.com/NicolasDortu/MorningStocks-Automatic-Email/assets/126513916/3fbbd2f3-cce2-4792-858a-7013f9c28750"/></th>
            </tr>
            <tr>
               <td colspan="6" style="text-align:left; padding: 4px;"><strong>News:</strong> <a href="https://www.businessinsider.com/big-short-michael-burry-john-paulson-gold-price-stock-portfolio-2024-5">Michael Burry and John Paulson hit the jackpot when they called the housing crash. Now they're betting on gold.</a><br/>Michael Burry bought about $8 million worth of a trust that owns physical gold bullion. John Paulson has been betting big on gold for years.</th>
            </tr>
            <tr>
               <th colspan="6" style="padding: 8px; text-align:center; font-size: 1.2em;"><strong>Crypto - Unweighted Average Variation: -1.83%</strong></th>
            </tr>
            <tr>
               <th style="text-align:center; padding: 4px;"><strong>BitCoin</strong></th>
               <th style="text-align:center; padding: 4px;">-1.83</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;">N/A</th>
               <th style="text-align:center; padding: 4px;"><img alt="BitCoin chart" src="https://github.com/NicolasDortu/MorningStocks-Automatic-Email/assets/126513916/42eecd28-5d58-4d56-af07-ea247ac99881"/></th>
            </tr>
            <tr>
               <td colspan="6" style="text-align:left; padding: 4px;"><strong>News:</strong> <a href="https://gizmodo.com/bitcoin-pizza-day-date-origin-history-cryptocurrency-1851487831">Everything to Know About Bitcoin Pizza Day</a><br/>On May 22, 2010, a man in Florida paid 10,000 Bitcoin for pizza.Read more...</th>
            </tr>
         </tbody>
         <tfoot>
            <tr>
               <th colspan="6" style="padding: 8px; text-align:center; font-size: 1.4em;"><strong>Total Unweighted Average Variation: -0.12%</strong></th>
            </tr>
         </tfoot>
      </table>
   </body>
</html>
