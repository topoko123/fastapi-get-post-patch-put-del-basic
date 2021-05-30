from fastapi import FastAPI

from pydantic import BaseModel            #Import BaseModel for receive

from typing import List, Optional

import uvicorn


class Item(BaseModel):                    
   name : Optional[str] = None
   description: Optional[str] = None
   price : Optional[float] = None

class Address(BaseModel):                #Collections of user address
   house_no     : str
   village_no   : str
   alley        : str
   lane         : str
   road         : str
   sub_district : str
   district     : str
   province     : str
   postal_code  : str

class UserBase(BaseModel):
   firstname : str
   lastname  : str
   age       : Optional[int] = None
   email     : Optional[str] = None
   address   : List[Address]              #List[Address]  <-- From class address(BaseModel)
   
class ListAll(BaseModel):
   list_user : List[UserBase]             #List[UserBase] <-- From class UserBase(BaseModel)

app = FastAPI()
   
items = {                            # Fake_db
   '1': {
      'name': 'mouse',
      'description': 'This is a Mouse',
      'price': 590,
   },
   '2': {
      'name': 'keyboard',
      'description': 'This is a Keyboard :)',
      'price': 3490
   }
}

@app.get('/items/{item_id}' )
async def read_item(item_id: str):
   if item_id == '0':
      return items
   else:
      return items[item_id]

@app.get('/fullname/{firstname}/{lastname}')
async def read_fullname(firstname: str, lastname: str):
   return firstname, lastname

@app.put('/items/{item_id}')
async def update_item(item_id: str, item: Item):         #Item is from class Item(BaseModel)
   items[item_id].update(**item.dict())
   msg = 'update success'
   return msg, item

@app.patch('/items/patch/{item_id}')
async def update_item_patch(item_id: str, item: Item):   #Item is from class Item(BaseModel)
   stored_item_data  = items[item_id]
   stored_item_model = Item(**stored_item_data)
   update_data       = item.dict(exclude_unset=True)
   update_item       = stored_item_model.copy(update=update_data)
   items[item_id]    = dict(update_item)
   return items[item_id]

@app.delete('/items/delete/{item_id}')
async def delete_item(item_id: str):
   items.pop(item_id)
   return 'delete success'


#------------------------------------------------------------------#
@app.post('/user', response_model=ListAll)
async def user(request: ListAll):            #ListAll is from class ListAll(BaseModel)
   return request

if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 



