#%%
import mario
import pandas as pd

from mario.tools.constants import _MASTER_INDEX as MI

from rules import _MASTER_SHEET_NAME as MS_name
from rules import _REGIONS_MAPS_SHEET_NAME as RMS_name
from rules import _MASTER_SHEET_COLUMNS as MS_cols
from rules import _REGIONS_MAPS_SHEET_COLUMNS as RMS_cols
from rules import _INVENTORY_SHEET_COLUMNS as InvS_cols

#%%
class DB_builder():

    def __init__(
        self,
        sut_db_path:str,
        sut_db_mode:str,
        master_file_path:str,
        get_master_file:bool = True,
    ):

        if sut_db_path.split('.')[-1] == 'txt':
            self.sut_db = mario.parse_from_txt(
                path=sut_db_path,
                table='SUT',
                mode=sut_db_mode,
            )
        if sut_db_path.split('.')[-1] == 'xlsx':
            self.sut_db = mario.parse_from_excel(
                path=sut_db_path,
                table='SUT',
                mode=sut_db_mode,
            )
        else:
            raise ValueError('This class is for "txt" or "xlsx" MARIO-readable databses')
        

        if get_master_file:
            self.get_fiona_master_template(path=master_file_path)
        else:
            self.read_master_file(path=master_file_path)
        
    def get_fiona_master_template(
        self,
        path:str,
        ):

        master_sheet = pd.DataFrame(columns=MS_cols)
        regions_maps_sheet = pd.DataFrame(self.sut_db.get_index(MI['r']), columns=RMS_cols) 

        with pd.ExcelWriter(path) as writer:
            master_sheet.to_excel(writer, sheet_name=MS_name, index=False)
            regions_maps_sheet.to_excel(writer, sheet_name=RMS_name, index=False)
    
    def read_master_file(
        self,
        path:str,
        get_inventories:bool = False,
        ):

        master_file = pd.read_excel(path,sheet_name=None,header=0,)

        self.master_sheet = master_file[MS_name].reset_index()
        self.regions_maps_sheet = master_file[RMS_name].reset_index()

        if get_inventories:
            self.get_fiona_inventory_templates(path=path)
    

    def get_fiona_inventory_templates(
        self,
        path:str,
    ):

        new_sheets = self.master_sheet['Sheet name'].unique()
        inventory_sheet = pd.DataFrame(columns=InvS_cols)

        with pd.ExcelWriter(path, mode='a', engine='openpyxl') as writer:
            for sheet in new_sheets:
                inventory_sheet.to_excel(writer, sheet_name=sheet, index=False)

        



#%%
if __name__ == '__main__':
    sut_db_path = 'tests/test_SUT.xlsx'
    sut_db_mode = 'flows'
    master_file_path = 'tests/master.xlsx'

    db = DB_builder(
        sut_db_path=sut_db_path,
        sut_db_mode=sut_db_mode,
        master_file_path=master_file_path,
        get_master_file=False,
    )

#%%
db.get_fiona_inventory_templates(path=master_file_path)


# %%
