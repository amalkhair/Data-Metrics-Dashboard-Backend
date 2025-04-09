import requests
import json
def download_file(url, filename):
    # open the url in read binary mode
    with requests.get(url) as response:
        # open the file in write binary mode
        with open(filename, 'wb') as file:
            # write the content of the response to the file
            file.write(response.content)


if __name__ == "__main__":
    total_count = 0
    result_is_not_empty = True
    page_nr = 1
    count_publication = 0
    publication_year = 0
    flag_year = 1700
    publication_all_years = 0
    while result_is_not_empty:
        url = f'https://api.openalex.org/works?filter=publication_year:1700-1710&sort=publication_date:asc&per-page=200&page={page_nr}'
        # print(f'Downloading page {page_nr}...')
        # print(url)

        with requests.get(url) as response:
            data = response.json()
            result_is_not_empty = len(data["results"]) > 0

            if result_is_not_empty:
                filename = f'data_{page_nr}.json'
                with open(filename, 'w') as file:
                    file.write(json.dumps(data))

                for result in data["results"]:
                    total_count += 1
                    publication_year = result["publication_year"]
                    if flag_year == publication_year:
                        count_publication += 1
                    else:
                        count_publication += 1
                        # print(f"Year changed to {flag_year} : {count_publication}")
                        # print(f'Number of publications in {flag_year}: {count_publication}')
                        # total_count += count_publication
                        print(f'Number publication of {flag_year}: {count_publication}')
                        publication_all_years += count_publication
                        count_publication = 0
                        flag_year = publication_year

            page_nr += 1


    print(f'Number publication of {flag_year}: {count_publication}')
    publication_all_years += count_publication

    print(f'Total number of publications: {total_count}')
    print(f"Publication All years: {publication_all_years}")
