from flask import Flask, render_template, request, redirect, url_for, session
import scraper
app = Flask(__name__)
app.secret_key = "XYZ"

@app.route('/start', methods = ['POST', 'GET'])
def startpage():
    if request.method == 'POST':
        
        search_info = request.form
        
        if ('searchtype' in search_info.keys()) and (search_info['fname'] != '') :
            search_type = search_info['searchtype']
            search_term = search_info['fname']
            search_pageination = 1
            if 'pageination' in search_info.keys():
                search_pageination = 2

            
            if search_type == 'scraper':
                scrape_results = scraper.scrape_github(search_term = search_term)
                
            else:
                scrape_results = scraper.github_api(search_term = search_term, num_pages=search_pageination)
            
            if scrape_results == []:
                return redirect(url_for("no_result"))

            else:    
                session['results'] = scrape_results
                return redirect(url_for("resultpage"))
    
    return render_template('startpage.html')

@app.route('/resultpage', methods = ['POST', 'GET'])
def resultpage():
    return render_template("resultpage.html", results = session.pop('results', None))

@app.route('/no_result', methods = ['POST', 'GET'])
def no_result():
    return render_template("no_result.html", results = session.pop('results', None))

if __name__ == '__main__':
   app.run(debug=True)