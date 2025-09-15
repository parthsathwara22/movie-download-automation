from DrissionPage import ChromiumOptions, ChromiumPage
import os

download_dir = r"D:\parth\movies" # change this
os.makedirs(download_dir, exist_ok=True)

co = ChromiumOptions().set_browser_path(
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
)
co.set_argument('--safebrowsing-disable-download-protection')
co.set_pref('download.default_directory', download_dir)
co.set_pref('download.prompt_for_download', False)
co.set_pref('download.directory_upgrade', True)
co.set_pref('safebrowsing.enabled', True)

def search_movie(movie_name):
    page = ChromiumPage(co)
    page.get("https://moviesmod.cafe/")
    search_bar = page.ele('xpath://input[@type="search"]')
    search_bar.click()
    search_bar.clear()
    search_bar.input(movie_name)
    page.actions.key_up('ENTER').key_down('ENTER')
    return page

def get_movie(movie_name):
    page = search_movie(movie_name)
    links = page.eles('xpath://h2[contains(@class, "title front-view-title")]//a')
    target = movie_name.lower().replace(" ", "-")
    for link in links:
        href = link.attr("href")
        if target in href:
            print("Found:", href)
            link.scroll()
            link.click(by_js=True)
            return page
    raise ValueError("Movie not found")

def movie_download_link(movie_name):
    page = get_movie(movie_name)
    for i in range(3, 0, -1):
        link = page.ele(f'xpath:(//a[contains(@class,"maxbutton-download-links")])[{i}]')
        if link:
            link.click()
            return page.latest_tab
    raise RuntimeError("No download links found")

def get_g_drive_link(movie_name):
    page = movie_download_link(movie_name)
    page.wait(6)

    link = page.ele('xpath://a[@class="maxbutton-1 maxbutton maxbutton-fast-server-gdrive"]')
    if link:
        link.attr("href")
        link.click()
    else:
        print("GDrive button not found")
    page.wait(3)
    new_page = page.browser.latest_tab
    return new_page

def get_loading_page(movie_name):
    page = get_g_drive_link(movie_name)
    page.wait(3)
    human_verification = page.ele('xpath:(//a)[8]')
    human_verification.click()
    page.wait(4)
    verify_button = page.ele('xpath://span[contains(text(), "Verify To Continue")]')
    verify_button.click()
    continue_btn = page.ele('xpath://span[contains(text(), "Click Here To Continue")]')
    continue_btn.click()
    download_btn = page.ele('xpath://a[contains (@class, "block cursor-pointer max-w-xs")]/@href')
    download_btn.click()

    new_page = page.browser.latest_tab
    return new_page

def get_final_download_link(movie_name):
    page = get_loading_page(movie_name)
    page.wait(10)
    instant_download = page.ele('xpath://a[contains(normalize-space(.), "Instant Download")]/@href')
    instant_download.click()
    new_page = page.browser.latest_tab
    return new_page

def get_the_final_link(movie_name):
    page = get_final_download_link(movie_name)
    link = page.ele('xpath://button[contains(text(), "Instant Download")]')
    link.click()
    page.wait(5)
    download_btn = page.ele('xpath://a[contains(text(), "Download Now")]')
    download_btn.click()
    return page

if __name__ == '__main__':
    movie = get_the_final_link('The Shawshank Redemption 1994') # Put movie name and it's release year
    movie.wait(250) # change this time according to your need
    movie.browser.quit()



