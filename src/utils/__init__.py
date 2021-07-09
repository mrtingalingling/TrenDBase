# # Add Sorting
# # https://developers.google.com/sheets/api/samples/data#sort_a_range_with_multiple_sorting_specifications
# # response = xyz.gsht_service.spreadsheets().get(spreadsheetId=spreadsheetId, ranges=[sheet_title], includeGridData=True).execute()
# # pp.pprint(response.get('sheets')[0].get('properties').get('sheetId'))
# sheetId = sheet_info.get('replies')[0].get('addSheet').get('properties').get('sheetId')
# data_body = {
#     'requests': [
#         {
#             "sortRange": {
#                 "range": {
#                     "sheetId": sheetId,
#                     "startRowIndex": 1,
#                 },
#                 "sortSpecs": [
#                     {
#                         "dimensionIndex": 0,  # Job Name
#                         "sortOrder": "ASCENDING"
#                     },
#                     {
#                         "dimensionIndex": 1,  # iodepth
#                         "sortOrder": "ASCENDING"
#                     },
#                     {
#                         "dimensionIndex": 2,  # bs
#                         "sortOrder": "ASCENDING"
#                     },
#                     {
#                         "dimensionIndex": 3,  # rw
#                         "sortOrder": "ASCENDING"
#                     },
#                     {
#                         "dimensionIndex": 6,  # rwmixread
#                         "sortOrder": "ASCENDING"
#                     }
#                 ]
#             }
#         }
#     ]
# }
# xyz.gsht_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=data_body).execute()
