import csv

from fpdf import FPDF

emoji_map = [a + " " + b for a, b in zip(["blue"] * 4 + ["orange"] * 4 + ["green"] * 4 + ["red"] * 4 + ["black"] * 4,
    ["*", "♥", "@", "█"] * 5)]


class EmojiCutoutDocument(FPDF):

    def __init__(self):
        super().__init__()
        self.w = 210
        self.h = 297
        self.is_at_line_start = True
        self.set_line_width(0.0)
        self.add_font('DejaVu', fname='fonts/DejaVuSansCondensed.ttf', uni=True)
        # self.add_font('heb', fname='fonts/GveretLevinAlefAlefAlef-Regular.ttf', uni=True)
        # self.add_font('heb', fname='fonts/NotoSerifHebrew-SemiCondensedBlack.ttf', uni=True)
        # self.add_font('emoji', fname='fonts/emoji.ttf', uni=True)
        self.set_font('DejaVu', size=12)

        self.current_height = 0

    def add_person_note(self, person_name: str, emojis: list):
        self.set_text_color(0, 0, 0)
        self.write(txt="".join(reversed(person_name)) + "   ")
        for emoji in emojis:
            color = emoji.split(" ")[0]
            if color == "black":
                self.set_text_color(0, 0, 0)
            elif color == "blue":
                self.set_text_color(0, 0, 200)
            elif color == "red":
                self.set_text_color(200, 0, 0)
            elif color == "green":
                self.set_text_color(0, 200, 0)
            elif color == "orange":
                self.set_text_color(255, 127, 0)
            self.write(txt=emoji.split(" ")[1] + " ")
        self.multi_cell(w=self.w/6, h=self.font_size*1.8, ln=3 if self.is_at_line_start else 1, border=0)
        self.is_at_line_start = not self.is_at_line_start


class RowConverter(object):

    def __init__(self, headers_list: list, name_column_in_csv: int, first_flag_column: int):
        self._headers_list = headers_list
        self._name_column_in_csv = name_column_in_csv
        self._first_flag_column = first_flag_column

    def convert_flag_to_symbol(self, index: int):
        if (len(emoji_map) > index - self._first_flag_column):
            return emoji_map[index - self._first_flag_column]
        else:
            return self._headers_list[index]

    def parse_relevant_categories_from_line(self, response_row: list):
        line_owner_name = response_row[self._name_column_in_csv]
        category_collection = []
        for flag_index in range(self._first_flag_column, len(response_row)):
            if str(response_row[flag_index]).lower() == "true":
                category_collection += [self.convert_flag_to_symbol(flag_index)]
        return line_owner_name, category_collection


def parse_csv_and_make_notes(filename: str, name_column_in_csv: int, first_flag_column: int):
    name_to_emoji_dictionary = {}
    with open(filename, "r", encoding="utf-8") as responses:
        row_converter = None
        csv_reader = csv.reader(responses, delimiter=',')
        line_counter = 0
        for response_row in csv_reader:
            if line_counter == 0:
                row_converter = RowConverter(response_row, name_column_in_csv, first_flag_column)
                for flag_index in range(first_flag_column, len(response_row)):
                    print(response_row[flag_index] + ": " + emoji_map[flag_index - first_flag_column])
                print(len(response_row) - first_flag_column)
                line_counter += 1
            else:
                name_mapping = row_converter.parse_relevant_categories_from_line(response_row)
                name_to_emoji_dictionary[name_mapping[0]] = name_mapping[1]
    return name_to_emoji_dictionary


if __name__ == "__main__":
    nte_dict = parse_csv_and_make_notes("responses.csv", name_column_in_csv=1, first_flag_column=23)
    pdf_output = EmojiCutoutDocument()
    pdf_output.add_page()
    for name in nte_dict.keys():
        print(", ".join(nte_dict[name]))
        pdf_output.add_person_note(name, nte_dict[name])
        # break
    pdf_output.output("test.pdf")
