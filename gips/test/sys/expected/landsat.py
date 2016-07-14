"""Known-good outcomes for tests, mostly stdout and created files."""

# trailing whitespace and other junk characters are in current output
t_info = { 'stdout':  """\x1b[1mGIPS Data Repositories (v0.8.2)\x1b[0m
\x1b[1m
Landsat Products v0.9.0\x1b[0m
  Optional qualifiers listed below each product.
  Specify by appending '-option' to product (e.g., ref-toa)
\x1b[1m
Index Products
\x1b[0m   bi          Brightness Index                        
                 toa: use top of the atmosphere reflectance
   evi         Enhanced Vegetation Index               
                 toa: use top of the atmosphere reflectance
   lswi        Land Surface Water Index                
                 toa: use top of the atmosphere reflectance
   msavi2      Modified Soil-Adjusted Vegetation Index (revised)
                 toa: use top of the atmosphere reflectance
   ndsi        Normalized Difference Snow Index        
                 toa: use top of the atmosphere reflectance
   ndvi        Normalized Difference Vegetation Index  
                 toa: use top of the atmosphere reflectance
   ndwi        Normalized Difference Water Index       
                 toa: use top of the atmosphere reflectance
   satvi       Soil-Adjusted Total Vegetation Index    
                 toa: use top of the atmosphere reflectance
\x1b[1m
LC8SR Products
\x1b[0m   ndvi8sr     Normalized Difference Vegetation from LC8SR
\x1b[1m
Tillage Products
\x1b[0m   crc         Crop Residue Cover                      
                 toa: use top of the atmosphere reflectance
   isti        Inverse Standard Tillage Index          
                 toa: use top of the atmosphere reflectance
   ndti        Normalized Difference Tillage Index     
                 toa: use top of the atmosphere reflectance
   sti         Standard Tillage Index                  
                 toa: use top of the atmosphere reflectance
\x1b[1m
Standard Products
\x1b[0m   acca        Automated Cloud Cover Assessment        
                 X: erosion kernel diameter in pixels (default: 5)
                 Y: dilation kernel diameter in pixels (default: 10)
                 Z: cloud height in meters (default: 4000)
   bqa         LC8 band quality                        
   bqashadow   LC8 QA + Shadow Smear                   
                 X: erosion kernel diameter in pixels (default: 5)
                 Y: dilation kernel diameter in pixels (default: 10)
                 Z: cloud height in meters (default: 4000)
   dn          Raw digital numbers                     
   fmask       Fmask cloud cover                       
   landmask    Land mask from LC8SR                    
   rad         Surface-leaving radiance                
                 toa: use top of the atmosphere reflectance
   ref         Surface reflectance                     
                 toa: use top of the atmosphere reflectance
   tcap        Tassled cap transformation              
   temp        Brightness (apparent) temperature       
   volref      Volumetric water reflectance - valid for water only
                 toa: use top of the atmosphere reflectance
   wtemp       Water temperature (atmospherically correct) - valid for water only
"""}
