# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:49:21 2019

@author: sklose
"""


    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(16, 8))
    plt.subplot2grid((2,1),(0,0))
    #plt.plot(time_dsm+1900, Total_cu_outflow_app[:,:,:,0,0].sum(axis=0).sum(axis=0),'b')
    plt.plot(time_dsm+1900, Total_cu_outflow_app[:,:,:,1,0].sum(axis=0).sum(axis=0),'g')
    plt.plot(time_dsm+1900, Total_cu_outflow_app[:,:,:,2,0].sum(axis=0).sum(axis=0),'r')
    #plt.plot(time_dsm+1900, Total_cu_outflow_app[:,:,:,0,1].sum(axis=0).sum(axis=0),'b--')
    plt.plot(time_dsm+1900, Total_cu_outflow_app[:,:,:,1,1].sum(axis=0).sum(axis=0),'g--')
    plt.plot(time_dsm+1900, Total_cu_outflow_app[:,:,:,2,1].sum(axis=0).sum(axis=0),'r--')
    plt.ylabel('Cu outflow [kt/year]')

    
    plt.subplot2grid((2,1),(1,0))
    #plt.plot(time_dsm+1900, Total_cu_inflow_app[:,:,:,0,0].sum(axis=0).sum(axis=0),'b')
    plt.plot(time_dsm+1900, Total_cu_inflow_app[:,:,:,1,0].sum(axis=0).sum(axis=0),'g')
    plt.plot(time_dsm+1900, Total_cu_inflow_app[:,:,:,2,0].sum(axis=0).sum(axis=0),'r')
    #plt.plot(time_dsm+1900, Total_cu_inflow_app[:,:,:,0,1].sum(axis=0).sum(axis=0),'b--')
    plt.plot(time_dsm+1900, Total_cu_inflow_app[:,:,:,1,1].sum(axis=0).sum(axis=0),'g--')
    plt.plot(time_dsm+1900, Total_cu_inflow_app[:,:,:,2,1].sum(axis=0).sum(axis=0),'r--')
    plt.ylabel('Cu inflow [kt/year]')

    legend= ['SSP 1 unmitigated','SSP 2 unmitigated','SSP 1 RCP2.6 ','SSP 2 RCP2.6 ']
    fig.legend(  labels=legend,   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1,    # Small spacing around legend box
       #    title="Legend Title"  # Title for the legend
           )
    plt.show()
    
    
    
    
    
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    plt.subplot2grid((2,2),(0,0))
    plt.stackplot(time_dsm+1900, Total_cu_outflow_app[:,:,:,1,0].sum(axis=0))
    plt.title('Cu outflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[1] +' '+ IndexTable.Classification['Scenario_RCP'].Items[0]  )
    plt.ylabel('Cu outflow [kt/year]')

  #  Figurecounter += 1

    plt.subplot2grid((2,2),(0,1))
    plt.stackplot(time_dsm+1900, Total_cu_outflow_app[:,:,:,1,1].sum(axis=0))
    plt.title('Cu outflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[1] +' '+  IndexTable.Classification['Scenario_RCP'].Items[1]  )
   #     plt.ylabel('Cu outflow [kt/year]')

  #  Figurecounter += 1
    
    plt.subplot2grid((2,2),(1,0))
    plt.stackplot(time_dsm+1900, Total_cu_outflow_app[:,:,:,2,0].sum(axis=0))
    plt.title('Cu outflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[2] +' '+  IndexTable.Classification['Scenario_RCP'].Items[0]  )
    plt.ylabel('Cu outflow [kt/year]')

 #   Figurecounter += 1
    
    plt.subplot2grid((2,2),(1,1))
    plt.stackplot(time_dsm+1900, Total_cu_outflow_app[:,:,:,2,1].sum(axis=0))
    plt.title('Cu outflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[2] +' '+  IndexTable.Classification['Scenario_RCP'].Items[1]  )
  #  plt.ylabel('Cu outflow [kt/year]')

    #Figurecounter += 1
 #  lgd = legend(hL,[h1;h2;h3;h4],'RandomPlot1','RandomPlot2','RandomPlot3','RandomPlot4');
#        set(lgd,'position',poshL);
#  

    line_labels = ['Fan',
                   'Air-cooler',
                   'Air-conditioning',
                   'Refridgerator',
                   'Microwave',
                   'Washing Machine',
                   'Tumble dryer',
                   'Dish washer',
                   'Television',
                   'VCR/DVD player',
                   'PC & Laptop computers']
  #  box = fig.get_position()
   #     fig.set_position([box.x0, box.y0 + box.height * 0.1,
       #      box.width, box.height * 0.9])

# Put a legend below current axis
    plt.legend(labels=line_labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
      fancybox=True, shadow=True, ncol=5)
  #  fig.legend(  labels=line_labels,   # The labels for each line
   ##    loc="center left",   # Position of legend
    #   borderaxespad=0.1,    # Small spacing around legend box
   #    title="Legend Title"  # Title for the legend
   #    bbox_to_anchor=(1, 0.5))
    

    plt.show()
    
    
    
    
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    plt.subplot2grid((2,2),(0,0))
    plt.stackplot(time_dsm+1900, Total_cu_inflow_app[:,:,:,1,0].sum(axis=0))
    plt.title('Cu inflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[1] +' '+ IndexTable.Classification['Scenario_RCP'].Items[0]  )
    plt.ylabel('Cu outflow [kt/year]')

  #  Figurecounter += 1

    plt.subplot2grid((2,2),(0,1))
    plt.stackplot(time_dsm+1900, Total_cu_inflow_app[:,:,:,1,1].sum(axis=0))
    plt.title('Cu inflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[1] +' '+  IndexTable.Classification['Scenario_RCP'].Items[1]  )
   #     plt.ylabel('Cu outflow [kt/year]')

  #  Figurecounter += 1
    
    plt.subplot2grid((2,2),(1,0))
    plt.stackplot(time_dsm+1900, Total_cu_inflow_app[:,:,:,2,0].sum(axis=0))
    plt.title('Cu inflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[2] +' '+  IndexTable.Classification['Scenario_RCP'].Items[0]  )
    plt.ylabel('Cu outflow [kt/year]')

 #   Figurecounter += 1
    
    plt.subplot2grid((2,2),(1,1))
    plt.stackplot(time_dsm+1900, Total_cu_inflow_app[:,:,:,2,1].sum(axis=0))
    plt.title('Cu inflow for Sector appliances '+ IndexTable.Classification['Scenario'].Items[2] +' '+  IndexTable.Classification['Scenario_RCP'].Items[1]  )
  #  plt.ylabel('Cu outflow [kt/year]')

    #Figurecounter += 1
 #  lgd = legend(hL,[h1;h2;h3;h4],'RandomPlot1','RandomPlot2','RandomPlot3','RandomPlot4');
#        set(lgd,'position',poshL);
#  

    line_labels = ['Fan',
                   'Air-cooler',
                   'Air-conditioning',
                   'Refridgerator',
                   'Microwave',
                   'Washing Machine',
                   'Tumble dryer',
                   'Dish washer',
                   'Television',
                   'VCR/DVD player',
                   'PC & Laptop computers']
  #  box = fig.get_position()
  #  box = fig.get_position()
   #     fig.set_position([box.x0, box.y0 + box.height * 0.1,
       #      box.width, box.height * 0.9])

# Put a legend below current axis
    plt.legend(labels=line_labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
      fancybox=True, shadow=True, ncol=5)
  #  fig.legend(  labels=line_labels,   # The labels for each line
   ##    loc="center left",   # Position of legend
    #   borderaxespad=0.1,    # Small spacing around legend box
   #    title="Legend Title"  # Title for the legend
   #    bbox_to_anchor=(1, 0.5))
    

    plt.show()
    

            
    