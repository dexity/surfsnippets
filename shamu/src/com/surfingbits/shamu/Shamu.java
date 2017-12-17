package com.surfingbits.shamu;

import java.util.HashMap;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import java.util.Random;

public class Shamu extends Activity {
    /** Called when the activity is first created. */
	
	HashMap<Integer, String> num2pic;
	private static Random randNum;
	public static int randl, randr;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        initValues();
             
        Button btnLeft = (Button) findViewById(R.id.button_left);  // Left button      
        btnLeft.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View v) {
            	Shamu.this.replaceImage("l");
            }
        });
        Button btnRight = (Button) findViewById(R.id.button_right); // Right button
        btnRight.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View v) {
            	Shamu.this.replaceImage("r");
            }
        });
    }
    
    public void initValues()
    {
        randNum	= new Random();
        randl	= 0;
        randr	= 0;
	    num2pic = new HashMap<Integer, String>();
	    num2pic.put(new Integer(0), "shamu");
	    num2pic.put(new Integer(1), "dolphin");
	    num2pic.put(new Integer(2), "seastar");
	    num2pic.put(new Integer(3), "rayfish");
    }
    
    public int getRandNum(String side)
    {
    	// Two static variables randl and randr are set by corresponding button
        try {
	    	int temp 	= Shamu.class.getField("rand"+side).getInt(null);	// randr or randl
	        int tempB	= temp;
	        while (tempB == temp)
	        {	// try until you get different int 
	            temp    = randNum.nextInt(num2pic.size());
	        }
	        Shamu.class.getField("rand"+side).setInt(Shamu.class, temp);
	        return temp;
        } catch (NoSuchFieldException e) {
		    return 0;
		} catch (SecurityException e) {
		    return 0;
		} catch (IllegalAccessException e) {
		    return 0;
		}
    }    
    
    public int layoutId(String base, Class cls, String side)
    {	
    	// Trying to use reflection getField (similar to Python getattr) to get field value
    	int id;
    	// Check if side is "l" or "r"
    	try {
    		id	= cls.getField(base+"_"+side).getInt(null);	// Example: R.id.picture_l
    	} catch (NoSuchFieldException e) {
		    id = 0;
		} catch (SecurityException e) {
		    id = 0;
		} catch (IllegalAccessException e) {
		    id = 0;
		}
    	return id;
    }
    
    
    public void replaceImage(String side)
    {
    	ImageView pic	= (ImageView) findViewById(layoutId("picture", R.id.class, side)); // R.id.picture_lXXX: Fix picture
    	pic.setImageResource(layoutId(num2pic.get(getRandNum(side)), R.drawable.class, side));	//R.drawable.shamu_l);
    }
}
