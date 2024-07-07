from dataclasses import dataclass
import os
from sortgs import *
from datetime import datetime


@dataclass(frozen=True)
class GetPaperListFromGoogleScholar:
    keyword: str
    nresults: int = 100
    save_csv: str = True
    csvpath: str = os.getcwd()
    sortby: str = "Citations"  # "Year"
    plot_results: bool = False
    start_year: str | None = None
    end_year: str = datetime.now().year
    debug: bool = False


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ja",
    "Cache-Control": "max-age=0",
    "Cookie": "NID=515=jwZSPDxENfRTAa3MCvAzSEYT8dqJdEvnkIjQhyC5qfzHTrJZqShEIZ3nxAyUgW3ibe54uv_uPmqWMuBBtF9nrZGyVL8sqDhMDBYUaTtPZOwlX3uP1S0o0GRUsKrq1wxhJKda6mNad4vyTGvVnanJaboLbz8FCqlmTG2TUnlSwB0; GSP=LM=1720346876:S=2Kea8LkoRTm5h8Rq",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "Sec-Ch-Ua-Arch": '"x86"',
    "Sec-Ch-Ua-Bitness": '"64"',
    "Sec-Ch-Ua-Full-Version-List": '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Model": '""',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
    "Sec-Ch-Ua-Wow64": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}
# {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}


def main(parameter: GetPaperListFromGoogleScholar):
    # Get command line arguments
    keyword = parameter.keyword
    number_of_results = parameter.nresults
    save_database = parameter.save_csv
    path = parameter.csvpath
    sortby_column = parameter.sortby
    plot_results = parameter.plot_results
    start_year = parameter.start_year
    end_year = parameter.end_year
    debug = parameter.debug

    print("Running with the following parameters:")
    print(
        f"Keyword: {keyword}, Number of results: {number_of_results}, Save database: {save_database}, Path: {path}, Sort by: {sortby_column}, Plot results: {plot_results}, Start year: {start_year}, End year: {end_year}, Debug: {debug}"
    )

    # Create main URL based on command line arguments
    if start_year:
        GSCHOLAR_MAIN_URL = GSCHOLAR_URL + STARTYEAR_URL.format(start_year)
    else:
        GSCHOLAR_MAIN_URL = GSCHOLAR_URL

    if end_year != now.year:
        GSCHOLAR_MAIN_URL = GSCHOLAR_MAIN_URL + ENDYEAR_URL.format(end_year)

    if debug:
        GSCHOLAR_MAIN_URL = "https://web.archive.org/web/20210314203256/" + GSCHOLAR_URL

    # Start new session
    session = requests.Session()
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # Variables
    links = []
    title = []
    citations = []
    year = []
    author = []
    venue = []
    publisher = []
    rank = [0]

    # Get content from number_of_results URLs
    for n in range(0, number_of_results, 10):
        # if start_year is None:
        url = GSCHOLAR_MAIN_URL.format(str(n), keyword.replace(" ", "+"))
        if debug:
            print("Opening URL:", url)
        # else:
        #    url=GSCHOLAR_URL_YEAR.format(str(n), keyword.replace(' ','+'), start_year=start_year, end_year=end_year)

        print("Loading next {} results".format(n + 10))
        page = session.get(url, headers=headers)
        c = page.content

        if any(kw in c.decode("ISO-8859-1") for kw in ROBOT_KW):
            # print("--------------------------")
            # for kw in ROBOT_KW:
            #     if kw in c.decode("ISO-8859-1"):
            #         print("Keyword {} detected".format(kw))

            try:
                c = get_content_with_selenium(url)
            except Exception as e:
                print("No success. The following error was raised:")
                print(e)

        # # Create parser
        soup = BeautifulSoup(c, "html.parser", from_encoding="utf-8")

        # Get stuff
        mydivs = soup.findAll("div", {"class": "gs_or"})

        for div in mydivs:
            try:
                links.append(div.find("h3").find("a").get("href"))
            except:  # catch *all* exceptions
                links.append("Look manually at: " + url)

            try:
                title.append(div.find("h3").find("a").text)
            except:
                title.append("Could not catch title")

            try:
                citations.append(get_citations(str(div.format_string)))
            except:
                warnings.warn("Number of citations not found for {}. Appending 0".format(title[-1]))
                citations.append(0)

            try:
                year.append(get_year(div.find("div", {"class": "gs_a"}).text))
            except:
                warnings.warn("Year not found for {}, appending 0".format(title[-1]))
                year.append(0)

            try:
                author.append(get_author(div.find("div", {"class": "gs_a"}).text))
            except:
                author.append("Author not found")

            try:
                publisher.append(div.find("div", {"class": "gs_a"}).text.split("-")[-1])
            except:
                publisher.append("Publisher not found")

            try:
                venue.append(" ".join(div.find("div", {"class": "gs_a"}).text.split("-")[-2].split(",")[:-1]))
            except:
                venue.append("Venue not fount")

            rank.append(rank[-1] + 1)

        # Delay
        sleep(0.5)

    # Create a dataset and sort by the number of citations
    data = pd.DataFrame(
        list(zip(author, title, citations, year, publisher, venue, links)),
        index=rank[1:],
        columns=["Author", "Title", "Citations", "Year", "Publisher", "Venue", "Source"],
    )
    data.index.name = "Rank"

    # Avoid years that are higher than the current year by clipping it to end_year
    data["cit/year"] = data["Citations"] / (end_year + 1 - data["Year"].clip(upper=end_year))
    data["cit/year"] = data["cit/year"].round(0).astype(int)

    # Sort by the selected columns, if exists
    try:
        data_ranked = data.sort_values(by=sortby_column, ascending=False)
    except Exception as e:
        print("Column name to be sorted not found. Sorting by the number of citations...")
        data_ranked = data.sort_values(by="Citations", ascending=False)
        print(e)

    # Print data
    print(data_ranked)

    # Plot by citation number
    if plot_results:
        plt.plot(rank[1:], citations, "*")
        plt.ylabel("Number of Citations")
        plt.xlabel("Rank of the keyword on Google Scholar")
        plt.title("Keyword: " + keyword)
        plt.show()

    # Save results
    if save_database:
        fpath_csv = os.path.join(path, keyword.replace(" ", "_") + ".csv")
        fpath_csv = fpath_csv[:MAX_CSV_FNAME]
        data_ranked.to_csv(fpath_csv, encoding="utf-8")
        print("Results saved to", fpath_csv)


if __name__ == "__main__":
    keyword = "'MITRE ATTACK Framework' 'Detection'"

    main(GetPaperListFromGoogleScholar(keyword, 1000, True, os.getcwd(), "Rank", False, 2022, datetime.now().year, False))
