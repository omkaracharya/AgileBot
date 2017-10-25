# Helper for xpath queries.

next_message_xpath = '../../../../following-sibling::ts-message'


def get_latest_sent_message(action):
    return str.format(
        '(//div[@class="message_content"]//span[@class="message_body"][starts-with(text(),'
        '" {}")]/..//div[@class="message_content_header_left"]//a[text()="Tester"])[last()]', action.command)
