def check_elem(self,func_name,elem,elem_name):
         #For easy debugging
        if not elem:
            errMsg="In "+func_name+","+elem_name+" Not Found."
            raise Exception(errMsg)