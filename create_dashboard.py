import csv
import json
from collections import defaultdict

# Load CSV data manually
def load_csv(filepath):
    data = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean up empty values
            row = {k: v for k, v in row.items() if v}
            if row:
                data.append(row)
    return data

# Load data
df = load_csv('Teen_Mental_Health_Dataset.csv')

# Prepare data for analysis
def get_numeric_value(val):
    try:
        return float(val)
    except:
        return None

ages = [int(row['age']) for row in df if 'age' in row and row['age']]
genders = [row['gender'] for row in df if 'gender' in row and row['gender']]
platforms = [row['platform_usage'] for row in df if 'platform_usage' in row and row['platform_usage']]
stress_levels = [get_numeric_value(row['stress_level']) for row in df if 'stress_level' in row and row['stress_level']]
anxiety_levels = [get_numeric_value(row['anxiety_level']) for row in df if 'anxiety_level' in row and row['anxiety_level']]
addiction_levels = [get_numeric_value(row['addiction_level']) for row in df if 'addiction_level' in row and row['addiction_level']]
social_media_hours = [get_numeric_value(row['daily_social_media_hours']) for row in df if 'daily_social_media_hours' in row]
sleep_hours = [get_numeric_value(row['sleep_hours']) for row in df if 'sleep_hours' in row]
screen_time = [get_numeric_value(row['screen_time_before_sleep']) for row in df if 'screen_time_before_sleep' in row]

# Clean None values
stress_levels = [x for x in stress_levels if x is not None]
anxiety_levels = [x for x in anxiety_levels if x is not None]
addiction_levels = [x for x in addiction_levels if x is not None]
social_media_hours = [x for x in social_media_hours if x is not None]
sleep_hours = [x for x in sleep_hours if x is not None]
screen_time = [x for x in screen_time if x is not None]

# Calculate statistics
def mean(lst):
    return sum(lst) / len(lst) if lst else 0

def count_occurrences(lst):
    counts = defaultdict(int)
    for item in lst:
        counts[item] += 1
    return dict(counts)

# Generate HTML
html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teen Mental Health Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .metric-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        
        .metric-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .chart-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .chart-container h2 {
            background: #667eea;
            color: white;
            padding: 15px;
            margin: 0;
            font-size: 1.1em;
        }
        
        .chart {
            width: 100%;
            height: 400px;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Teen Mental Health Dashboard</h1>
            <p>Analysis of social media impact on teen mental health</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Total Teens Analyzed</h3>
                <div class="value">''' + str(len(df)) + '''</div>
            </div>
            <div class="metric-card">
                <h3>Avg Stress Level</h3>
                <div class="value">''' + f"{mean(stress_levels):.1f}" + '''/10</div>
            </div>
            <div class="metric-card">
                <h3>Avg Anxiety Level</h3>
                <div class="value">''' + f"{mean(anxiety_levels):.1f}" + '''/10</div>
            </div>
            <div class="metric-card">
                <h3>Avg Sleep Hours</h3>
                <div class="value">''' + f"{mean(sleep_hours):.1f}" + '''h</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <h2>Age Distribution</h2>
                <div id="ageChart" class="chart"></div>
            </div>
            
            <div class="chart-container">
                <h2>Gender Distribution</h2>
                <div id="genderChart" class="chart"></div>
            </div>
            
            <div class="chart-container">
                <h2>Mental Health Metrics</h2>
                <div id="mentalHealthChart" class="chart"></div>
            </div>
            
            <div class="chart-container">
                <h2>Platform Usage Distribution</h2>
                <div id="platformChart" class="chart"></div>
            </div>
            
            <div class="chart-container full-width">
                <h2>Social Media Hours vs Stress Level</h2>
                <div id="correlationChart" class="chart"></div>
            </div>
            
            <div class="chart-container full-width">
                <h2>Sleep Hours vs Screen Time Before Sleep</h2>
                <div id="sleepChart" class="chart"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Age Distribution
        var ageData = [''' + ','.join(str(a) for a in sorted(set(ages))) + '''];
        var ageCounts = {};
        ''' + '\n        '.join(f"ageCounts[{age}] = {ages.count(age)};" for age in sorted(set(ages))) + '''
        
        Plotly.newPlot('ageChart', [{
            x: Object.keys(ageCounts).map(x => parseInt(x)),
            y: Object.values(ageCounts),
            type: 'bar',
            marker: {color: '#667eea'}
        }], {
            margin: {l: 40, r: 40, t: 10, b: 40},
            xaxis: {title: 'Age'},
            yaxis: {title: 'Count'}
        }, {responsive: true});
        
        // Gender Distribution
''' + '''        var genderCounts = ''' + json.dumps(count_occurrences(genders)) + ''';
        Plotly.newPlot('genderChart', [{
            labels: Object.keys(genderCounts),
            values: Object.values(genderCounts),
            type: 'pie',
            marker: {colors: ['#667eea', '#764ba2', '#f093fb']}
        }], {
            margin: {l: 40, r: 40, t: 10, b: 40}
        }, {responsive: true});
        
        // Mental Health Metrics Box Plots
        var stressData = ''' + json.dumps([round(s, 1) for s in stress_levels]) + ''';
        var anxietyData = ''' + json.dumps([round(a, 1) for a in anxiety_levels]) + ''';
        var addictionData = ''' + json.dumps([round(ad, 1) for ad in addiction_levels]) + ''';
        
        Plotly.newPlot('mentalHealthChart', [
            {y: stressData, name: 'Stress', type: 'box', marker: {color: '#ff7f0e'}},
            {y: anxietyData, name: 'Anxiety', type: 'box', marker: {color: '#d62728'}},
            {y: addictionData, name: 'Addiction', type: 'box', marker: {color: '#9467bd'}}
        ], {
            margin: {l: 40, r: 40, t: 10, b: 40},
            yaxis: {title: 'Level (0-10)'}
        }, {responsive: true});
        
        // Platform Distribution
        var platformCounts = ''' + json.dumps(count_occurrences(platforms)) + ''';
        Plotly.newPlot('platformChart', [{
            labels: Object.keys(platformCounts),
            values: Object.values(platformCounts),
            type: 'pie',
            marker: {colors: ['#667eea', '#764ba2', '#f093fb']}
        }], {
            margin: {l: 40, r: 40, t: 10, b: 40}
        }, {responsive: true});
        
        // Correlation scatter plots
        var mediaHours = ''' + json.dumps([round(m, 1) for m in social_media_hours]) + ''';
        var stressForCorr = ''' + json.dumps([round(s, 1) for s in stress_levels[:len(social_media_hours)]]) + ''';
        
        Plotly.newPlot('correlationChart', [{
            x: mediaHours,
            y: stressForCorr,
            type: 'scatter',
            mode: 'markers',
            marker: {
                size: 8,
                color: stressForCorr,
                colorscale: 'Viridis',
                showscale: true
            }
        }], {
            margin: {l: 40, r: 40, t: 10, b: 40},
            xaxis: {title: 'Daily Social Media Hours'},
            yaxis: {title: 'Stress Level'}
        }, {responsive: true});
        
        // Sleep vs Screen Time
        var screenTimeData = ''' + json.dumps([round(s, 1) for s in screen_time]) + ''';
        var sleepHoursData = ''' + json.dumps([round(s, 1) for s in sleep_hours[:len(screen_time)]]) + ''';
        
        Plotly.newPlot('sleepChart', [{
            x: screenTimeData,
            y: sleepHoursData,
            type: 'scatter',
            mode: 'markers',
            marker: {
                size: 8,
                color: screenTimeData,
                colorscale: 'Reds',
                showscale: true
            }
        }], {
            margin: {l: 40, r: 40, t: 10, b: 40},
            xaxis: {title: 'Screen Time Before Sleep (hours)'},
            yaxis: {title: 'Sleep Hours'}
        }, {responsive: true});
    </script>
</body>
</html>'''

# Write HTML file
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Dashboard created successfully!")
print("📊 Open 'dashboard.html' in your browser to view the dashboard")
print(f"📈 Total records: {len(df)}")
print(f"😟 Average Stress Level: {mean(stress_levels):.1f}/10")
print(f"😰 Average Anxiety Level: {mean(anxiety_levels):.1f}/10")
print(f"😴 Average Sleep Hours: {mean(sleep_hours):.1f}h")
