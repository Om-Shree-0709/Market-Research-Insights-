import csv

def read_data_from_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            if len(row) == 6 and all(row):  
                try:
                    data.append({
                        'Year': int(row[0]),
                        'Website': row[1].strip(),
                        'Total Orders': int(row[2]),
                        'Total Returns': int(row[3]),
                        'Returns Due to Fit Issues': int(row[4]),
                        'Returns Due to Appearance Issues': int(row[5])
                    })
                except ValueError as e:
                    print(f"Error processing row: {row}. Error: {str(e)}")
    return data

def calculate_return_rate(total_returns, total_orders):
    return (total_returns / total_orders) * 100 if total_orders > 0 else 0

def calculate_percentage_returns_due_to_fit(total_fit_returns, total_returns):
    return (total_fit_returns / total_returns) * 100 if total_returns > 0 else 0

def analyze_data(data):
    results = []
    
    for row in data:
        return_rate = calculate_return_rate(row['Total Returns'], row['Total Orders'])
        percentage_fit_returns = calculate_percentage_returns_due_to_fit(row['Returns Due to Fit Issues'], row['Total Returns'])
        
        results.append({
            'Year': row['Year'],
            'Website': row['Website'],
            'Total Orders': row['Total Orders'],
            'Total Returns': row['Total Returns'],
            'Return Rate (%)': return_rate,
            'Returns Due to Fit (%)': percentage_fit_returns
        })
    
    return results

def compare_return_rates(results):
    summary = {}
    
    for result in results:
        website = result['Website']
        year = result['Year']
        return_rate = result['Return Rate (%)']
        
        if website not in summary:
            summary[website] = {}
        
        if year not in summary[website]:
            summary[website][year] = {
                'Total Orders': result['Total Orders'],
                'Total Returns': result['Total Returns'],
                'Return Rate (%)': return_rate,
                'Returns Due to Fit (%)': result['Returns Due to Fit (%)']
            }
    
    return summary

def write_results_to_csv(results, output_file):
    headers = ['Year', 'Website', 'Total Orders', 'Total Returns', 'Return Rate (%)', 'Returns Due to Fit (%)']
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def main(input_file, output_file):
    data = read_data_from_csv(input_file)
    results = analyze_data(data)
    summary = compare_return_rates(results)
    write_results_to_csv(results, output_file)
    
    print(f"Analysis completed. Results written to {output_file}")

if __name__ == "__main__":
    input_file = 'data.csv'  
    output_file = 'results.csv'  
    main(input_file, output_file)