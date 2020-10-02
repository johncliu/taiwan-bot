from datetime import datetime
import json
import logging

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import DefaultConfig

_logger = logging.getLogger(__name__)
CONFIG = DefaultConfig()


class TaiwanBotSheet:

    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    service_account_info_dict = json.loads(
        CONFIG.GOOGLE_SERVICE_ACCOUNT, strict=False)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        service_account_info_dict, scope)
    client = gspread.authorize(creds)

    def __init__(self):
        _logger.info('Initiating TaiwanBotSheet')

    def get_questions_answers(self, context):
        sheet = self.client.open(SPREADSHEET_FAQ).worksheet(context)
        questions = list(map(str.strip, sheet.col_values(1)[1:]))
        answers = list(map(str.strip, sheet.col_values(2)[1:]))

        return [questions, answers]

    def log_answers(self, context, user_question, similar_question, answer, score):
        sheet = self.client.open(SPREADSHEET_LOG).worksheet(context)
        next_row = len(sheet.get_all_values()) + 1
        sheet.update( 'A' + str(next_row) , datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        sheet.update( 'B' + str(next_row) , user_question)
        sheet.update( 'C' + str(next_row) , similar_question)
        sheet.update( 'D' + str(next_row) , answer)
        sheet.update( 'E' + str(next_row) , score)
