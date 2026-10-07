<!--

///***********************************************************************************
///* !!! IMPORTANT !!!
///* This is currently a hard linked file.  The 'real' file location is:
///* IAP_Program\Solutions\IAP\Implementation\Infrastructure\Framework\Webroot\IapWebBase\Includes
///***********************************************************************************

/// ***********************************************************************************
/// ** REVISION HISTORY
/// ***********************************************************************************
/// ** Revision Date		Author			Comments
/// ** --------------------------------------------------------------------------------
/// ** 12/27/2004			K. Fulgham		Created.  This file contains some common
///											javascript library functions used within Iap.
/// ** 01/20/2005			C. Pinheiro		Moved some functions from EubIapValidation 
///											here. Re-named functions to follow standards.
///											Created/modified common library functions.
/// ***********************************************************************************

/// ----------------------------------------------------------------------------------
/// Global Variable Declarations
/// ----------------------------------------------------------------------------------

// Stores the available window screen height 
var _EubIapCommonScreenHeight = "";

// Stores the available window screen width
var _EubIapCommonScreenWidth = "";

// Stores Index for accessing the menu form in the windows.frames() collection
var _EubIapFormMenu = 0;

// Stores Index for accessing the content form in the windows.frames() collection
var _EubIapFormContents = 1;

// Stores values and field names pairs in a object type array
var _EubIapEasOriginalValues = new Array();

/// *********************************************************************************************
/// *********************************************************************************************
/// EubIapCommon Functionality 
/// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

/// ----------------------------------------------------------------------------------
/// Window Functions
/// ----------------------------------------------------------------------------------

// Pauses the execution of javascript for a specified amount of time.
// numberMillis - Number of milliseconds to pause for.
function EubIapPagePause(numberMillis) 
{
	var dialogScript = 'window.setTimeout( function () { window.close(); }, ' +
		numberMillis + ');';

	var result = window.showModalDialog('javascript:document.writeln("<script>' +
		dialogScript + '<' + '/script>")');
}

/// ----------------------------------------------------------------------------------
/// String Functions
/// ----------------------------------------------------------------------------------

// Trims a string value for spaces in front and behind.
// stringValue - string value to reformat.
function EubIapCommonStripEmptySpaces(stringValue) 
{
	var firstFormat = "";
	var finalFormat = "";

	stringValue = String(stringValue);
	
	// Set regular expressions
	var frontExpression = /(\S+.*)/g; 
	var backExpression = /(.*\S{1})/g;

	// Trim the front of the string	
	firstFormat = stringValue.match(frontExpression);

	// If match does not result in null, then trim the back of the string.
	if (firstFormat != null) {
		// Trim the back of the string
		finalFormat = String(firstFormat).match(backExpression);

		// If match does not result in null, then return the string		
		if (finalFormat != null) {
			return finalFormat;
		}
		
		return "";
	}
	
	return "";
}

/// ----------------------------------------------------------------------------------
/// Window Control Functions
/// ----------------------------------------------------------------------------------

// Checks the length of a text area and makes sure that the length does not exceed the 
// limit allowed for that control. 
// textAreaControlToValidate - Textarea control to validate
// controlEvent - Any event that may have occurred
// maxLength - The max length allowed for this control
function EubIapCommonCheckMaxLength_KeyDown (textAreaControlToValidate, controlEvent, maxLength)
{
	if (document.selection.createRange().text.length > 0) { textAreaControlToValidate.selected = true; }
	
	if ((textAreaControlToValidate.selected && controlEvent.shiftKey) || controlEvent.ctrlKey || textAreaControlToValidate.selected) {
		textAreaControlToValidate.selected = false;
		return true;
	}

	var allowKey = false;
	var keyCode = document.layers ? controlEvent.which : controlEvent.keyCode;

	if (keyCode <= 46 && keyCode != 13)
		allowKey = true;
	else
		allowKey = textAreaControlToValidate.value.length < maxLength;

	textAreaControlToValidate.selected = false;
	return allowKey;
}

// Checks the length of a text area and makes sure that the 
// length does not exceed the limit allowed for that control.
// textAreaControlToValidate - Textarea control to validate
// maxLength - The max length allowed for this control
function EubIapCommonCheckMaxLength_KeyUp (textAreaControlToValidate, maxLength)
{
	if (textAreaControlToValidate.value.length > maxLength) {
		textAreaControlToValidate.value = textAreaControlToValidate.value.substr(0, maxLength);
	}
}

// Prevents the right-click of the mouse from displaying the context menu.
function EubIapCommonPreventRightClick() 
{
	// For development
	//return event.ctrlKey;
	
	// For production
	return false;
}

// Used to manage / prevent key combinations from being pressed.
function EubIapCommonPreventKeyboardCommands() 
{
	if (window.event.ctrlKey && window.event.keyCode == 78) 
	{
		event.returnValue = false;
	}
	
	// Prevent the enter key from being pressed on input controls (specifically textboxes)
	if (window.event.keyCode == 13 && window.event.srcElement != null) 
	{
		if (window.event.srcElement.tagName == "INPUT" && window.event.srcElement.type == "text") 
		{
			event.returnValue = false;
		}
	}
}

/// Sets all of the non button controls to enabled for post back
/// to ensure that the data is posted back.
function EubIapCommonEnableAllControls()
{
	var oFields = EubIapCommonGetMainForm().elements;
	
	for (i=0; i < oFields.length; i++)
	{
		if (EubIapCommonGetFieldType( oFields[i]) != "button") 
			EubIapCommonSetReadOnly(oFields[i].name, false);
	}
}

/// ----------------------------------------------------------------------------------
/// Common library setup
/// ----------------------------------------------------------------------------------

// Returns a handle to the main form tag.
function EubIapCommonGetMainForm()
{
	return _EubIapMainForm;
}

// Returns a handle to the main body tag.
function EubIapCommonGetBody()
{
	return _EubIapBody;
}

// Retrieves the screen width
function EubIapCommonGetScreenWidth() 
{
	return String(_EubIapCommonScreenWidth);
}

// Retrieves the screen height
function EubIapCommonGetScreenHeight() 
{
	return String(_EubIapCommonScreenHeight);
}

// Determine available size of screen based upon user's resolution
function EubIapCommonSetScreenSize() 
{
	if( this.frameElement == null )
	{
		//_EubIapCommonScreenWidth = this.window.screen.availWidth/2 -10; 
		//_EubIapCommonScreenHeight = this.window.screen.availHeight/2 - 28; 	
		_EubIapCommonScreenWidth = (this.window.screen.availWidth-(this.window.screenLeft*2))-10;
		_EubIapCommonScreenHeight = (this.window.screen.availHeight-(this.window.screenTop*2)) - 28;
	}else
	{
		_EubIapCommonScreenWidth = this.frameElement.offsetWidth -10; 
		_EubIapCommonScreenHeight = this.frameElement.offsetHeight - 28; 
	}
}

//	Sets up all of the global variables used by this library
function EubIapCommonSetGlobalObjects()
{
	_EubIapCommonScreenWidth = "0";
	_EubIapCommonScreenHeight = "0";
}

// Standard default setup of every page.  Its purpose is to handle any default 
// initialization needed for all pages, such as displaying server-side posted messages.
function EubIapCommonDefaultSetup() 
{

	// Sets the global objects
	EubIapCommonSetGlobalObjects();	
	
	// Sets the global screen variables 
	EubIapCommonSetScreenSize();
}

// Returns the MainFrame from DDS where EAS is contained
// Note - if DDS ever changes this frame name... we are in big trouble!!
function EubIapCommonGetDDSMainFrame()
{
	if (top.frames['frameMain'] == undefined)
	{
		return null;
	}
	else
	{
		return top.frames['frameMain'];
	}
}

// Returns the Menu Frame
function EubIapCommonGetMenuFrame()
{
	if (EubIapCommonGetDDSMainFrame() == null) 
	{
		return top;
	}
	else
	{
		return EubIapCommonGetDDSMainFrame().frames[_EubIapFormMenu];
	}
}

// Returns the Form Contents Frame
function EubIapCommonGetContentsFrame()
{
	if (EubIapCommonGetDDSMainFrame() == null) 
	{
		return top;
	}
	else
	{
		return EubIapCommonGetDDSMainFrame().frames[_EubIapFormContents];
	}
}

// Returns the target Location based on a Frame
function EubIapCommonGetTargetLocation()
{
	try
	{
		return _EubIapCommonTargetLocation;
	
	}catch(error)
	{
		//expected error - if javascripts includes have not been completly emitted yet
		//return the current document pathname
		if( error.description == "'_EubIapCommonTargetLocation' is undefined" )
			return document.location.pathname.substr(document.location.pathname.lastIndexOf('/')+1);
	}
}

function EubIapCommonGetPageHrefPath( CurrentPagePath )
{

	return CurrentPagePath.substr(0,CurrentPagePath.lastIndexOf("/"));
		
}

// Sets the isDirty flag for the page to indicate the client that changes have been made
function EubIapCommonSetIsPageDirty()
{
	if( EubIapCommonIsUndefined( _EubIapCommonIsPageDirty ) )
		_EubIapCommonIsPageDirty = false;
	else
		_EubIapCommonIsPageDirty = true;
		
}

// Sets the isDirty flag for the page to indicate the client that changes have been made
function EubIapCommonGetIsPageDirty()
{
	return _EubIapCommonIsPageDirty;
}

// Sets the given field disabled property Clears the contents of a field if the readOnlyFlag 
// is true and the control was not initially disabled.
// Regular usage:
//	- EubIapCommonSetReadOnly( fieldName, readOnlyFlag );
// There are two "optional" parameters:
//	- dontClearContentsFlag - when equals true will not clear the contents of the field being 
//	  enabled/disabled; Call EubIapCommonSetReadOnly( fieldName, readOnlyFlag, dontClearContentsFlag )
//	- dontSaveRestoreValues - when equals true will not save original saves and will not restore to 
//    original values (based on readOnly flag). Call EubIapCommonSetReadOnly( fieldName, readOnlyFlag, dontClearContentsFlag, dontSaveRestoreValues )
// Unfortunatelly Javascript does not support overloaded functions....
function EubIapCommonSetReadOnly( fieldName, readOnlyFlag, dontClearContentsFlag, dontSaveRestoreValues )
{
	var oControl = EubIapCommonGetControl( fieldName );
	var sType = EubIapCommonGetFieldType( oControl );
	var bInitDisabled = false;
	var ChildControl;

	var sNewCssClass = "";
	
	if( oControl == null )
		return;

	switch( sType )
	{
	
		case 'radio':
		{	
			//if single radio than
			if( EubIapCommonIsUndefined( oControl.length ) )
			{	
				bInitDisabled = oControl.disabled;
				oControl.disabled = readOnlyFlag;
				
			}else
			{
				for( i = 0; i < oControl.length; i++ )
				{	if( oControl[ i ].disabled )
						bInitDisabled = true;
					oControl[ i ].disabled = readOnlyFlag;
					//radio buttons display gray when disabled, no need for bckColor 
				}
			}
			break;
		}
		case "select-one":
		case "select-multiple" :
		{
			if( oControl.disabled )
				bInitDisabled = true;
			oControl.disabled = readOnlyFlag ;
			break;	
		}
		case "checkbox":
		{
			if( oControl.readOnly )
				bInitDisabled = true;
			oControl.readOnly = readOnlyFlag ;
			oControl.parentNode.readOnly = readOnlyFlag;
			break;	
		}
		case "checkboxlist":
		{
			sNewCssClass = oControl.getAttribute("CssDefault");
			
			for( var Index = 0; Index < oControl.all.length; Index++ )
			{
				ChildControl = oControl.all[ Index ];
				if( EubIapCommonGetFieldType( ChildControl ) == "checkbox" )
				{	//set label cssClass
					oControl.all[ Index + 1 ].className = sNewCssClass
					EubIapCommonSetReadOnly( ChildControl.id, readOnlyFlag, dontClearContentsFlag );
				
				}
			}
			break;
		}
		case "SqlValueDatePicker":
		{	
			SqlValueDatePickerSetReadOnly( fieldName, readOnlyFlag, dontClearContentsFlag );
			break;
			
		}
		case "button":
		case "submit":
		{
			if( readOnlyFlag )
				EubIapCommonDisableButton( oControl );
			else
				EubIapCommonEnableButton( oControl );
				
			break;
		}
		default:
		{
			if( oControl.readOnly )
				bInitDisabled = true;
			oControl.readOnly = readOnlyFlag ;
			break;
		}
	}
	
	//set css class
	EubIapCommonSetCssClassName( oControl, sType, readOnlyFlag );
	
	if( dontClearContentsFlag != true )
	{	if( ( !bInitDisabled ) && ( readOnlyFlag ) )
			EubIapCommonClearFieldContents( oControl );
	}
}

// Sets the class attribute of a given control
function EubIapCommonSetCssClassName( Control, Type, readOnlyFlag )
{
	var sNewCssClass;
	
	switch( Type )
	{
		case "checkbox":
		{
			if(readOnlyFlag)
				sNewCssClass = Control.parentNode.getAttribute("CssDisabled");
			else
				sNewCssClass = Control.parentNode.getAttribute("CssDefault");
				
			Control.parentNode.className = sNewCssClass;
			break;
		}
		case "radio":
		case "button":
		case "submit":
		{
			break;
		}
		default:
		{
			if(readOnlyFlag)
				sNewCssClass = Control.getAttribute("CssDisabled");
			else
				sNewCssClass = Control.getAttribute("CssDefault");
				
			Control.className = sNewCssClass
		}
	}	
}

// Saves or restores the value of a given control into an array
function EubIapCommonSaveOriginalValues( fieldName, RestoreValue, ReSave )
{
	var OriginalData =  new Object();
	var value;
	var Index;
	
	value = EubIapCommonGetFieldValue( fieldName,"Value" );
	
	//Check if field is already on origibal values list
	if( ( EubIapCommonIsUndefined( _EubIapEasOriginalValues[ fieldName ] ) ) || ( ReSave == true ) )
	{
		//Only save original value when is not undefined and not blank.
		if( !EubIapCommonIsUndefined( value ) && !EubIapCommonIsBlank( value ) )
		{	
			//if not add it!!
			OriginalData.fieldName = fieldName;
			OriginalData.fieldValue = value;
			
			_EubIapEasOriginalValues[ fieldName ] = OriginalData;
		}
	}
	
	if( RestoreValue )
	{
		if( EubIapCommonIsUndefined( _EubIapEasOriginalValues[ fieldName ] ) )
			return;
			
		EubIapValidationSetFieldValue( fieldName, "Value", _EubIapEasOriginalValues[ fieldName ].fieldValue );
	}
}

// Checks if a expression is empty or blank string
function EubIapCommonIsBlank( expression )
{
	if( expression == null || EubIapCommonIsUndefined( expression ) )
		return true;
		
	//sanity check
	expression = "" + expression + "";
	
	//When reading HTML - check for "blank space"
	if( expression == "&nbsp;" )
		return true;
	else
	{
		for(var iIndex = 0; iIndex < expression.length; iIndex++) 
		{
			var c = expression.charAt(iIndex);
			if ((c.trim() != '') && (c != '\n') && (c != '\t') && (c != '%'))
				return false;
		}
	}
		
	return true;
}

// Returns an Array of form field objects based on a field name
function EubIapCommonGetControlArray(p_sFieldName)
{  //if IE 4+
//   if(document.all)
//   {
//		var oControls = document.all(p_sFieldName);
//		var oArray;
//		
//		if ( oControls == null ) return;
//		// one control is returned
//		if ((oControls.length == undefined) && (oControls != undefined))
//		{
//			oArray = new Array();
//			oArray[0] = oControls;
//		}
//		//array of controls
//		else
//		{
//			oArray = oControls;
//		}
//      return  oArray; // document.all(p_sFieldName);
//   }
   //else //if netscape or others 
      var ch = document.forms[0].elements;
      var oArray = new Array();
      var iIndex, iCnt;
      iCnt = 0;
      for(iIndex = 0; iIndex < ch.length; iIndex++)
      {  
        if(ch[iIndex].id.toLowerCase() == p_sFieldName.toLowerCase())
         {  oArray[iCnt] = ch[iIndex];
            iCnt = iCnt + 1;
         }
      }
      return oArray;  
}

// Enable all buttons
function EubIapCommonEnableAllButtons()
{
	var aButtons = EubIapCommonGetControlArray("Button"); //array of button form fields
	
	if( EubIapCommonIsUndefined( aButtons ) )
	   return;
	
	for(iIndex = 0; iIndex < aButtons.length; iIndex++)
		EubIapCommonEnableButton(aButtons[iIndex]);
}

// HACK==> Need to bullet proof
function EubIapCommonGetField(p_Field)
{
	//var returnValue = null;
	//var field = "" + pField;
	//if (field.length > 0)
	//{
	//	returnValue = document.all[p_Field];
	//}
	//return returnValue;
	return document.all[p_Field];
}

// Enables a button object
function EubIapCommonEnableButton(p_oButton)
{
	if(p_oButton != null)	
	{
		p_oButton.disabled = false;
		p_oButton.style.backgroundColor = '#706C6C';
	}
	return true;
}

// Disables all buttons
function EubIapCommonDisableAllButtons()
{
	var aButtons = EubIapCommonGetControlArray("Button"); //array of button form fields
	
	if( EubIapCommonIsUndefined( aButtons ) )
	   return;
	    
	for(iIndex = 0; iIndex < aButtons.length; iIndex++)
		EubIapCommonDisableButton(aButtons[iIndex]);
		
}

// Disables a button object
function EubIapCommonDisableButton(p_oButton)
{	
	var Class = p_oButton.className;
	
	if(p_oButton != null)
	{
		if(p_oButton.disabled == false)
			p_oButton.style.backgroundColor = 'lightGrey';
		p_oButton.disabled = true;	
	}
	return true;
}

function EubIapCommonIsReadOnly(control)
{
	var oControl = EubIapCommonGetControl( control );
	var sType = EubIapCommonGetFieldType( oControl );
	var disabledInd = true;
	
	if ( oControl == null )
		return disabledInd;
		
	switch( sType )
	{
	
		case 'radio':
		{	
			//if single radio than
			if( EubIapCommonIsUndefined( oControl.length ) )
			{	
				disabledInd = oControl.disabled;
				
			}else
			{
				//assume that all radio's for a given control are disabled
				disabledInd = oControl[0].disabled;
			}
			break;
		}
		case "select-one":
		case "select-multiple" :
		{
			disabledInd = oControl.disabled;
			break;	
		}
		case "checkbox":
		{
			disabledInd = oControl.readOnly;
			break;	
		}
		case "checkboxlist":
		{
			//TODO - check
			disabledInd = oControl.disabled;
			break;
		}
		case "SqlValueDatePicker":
		{	
			//TODO - check
			disabledInd = oControl.disabled;
			break;
			
		}
		case "button":
		case "submit":
		{
			disabledInd = oControl.disabled;
			break;
		}
		default:
		{
			disabledInd = oControl.readOnly;
			break;
		}
	}
	return disabledInd;
}


// TODO - for all types, should return proper value (ie. int vs string)
function EubIapCommonGetFieldValue( control, property )
{
	var	sField = '';
	var oControl = EubIapCommonGetControl( control );
	var ChildControl;
	
	if( oControl == null )
		return "";

	if(	property.toUpperCase() == "VALUE" )
	{
		switch( EubIapCommonGetFieldType( oControl ) )
		{ 
			case "select-one"	:
				if( oControl.selectedIndex > -1 )
					sField = oControl.options[ oControl.selectedIndex ].value;
				else
					sField = "";
				break;
			case "select-multiple" :
				if( oControl.selectedIndex > -1 )
					sField = oControl.options[ oControl.selectedIndex ].value;
				else
					sField = "";
				break;
			case "radio" :
				sField = EubIapCommonGetRadioVal( oControl );
				break;
			case "checkbox"	:
				if( oControl.checked )
					sField = true;
				else
					sField = "";
				break;
			case "checkboxlist":
				sField = "";
				for( var Index = 0; Index < oControl.all.length; Index++ )
				{
					ChildControl = oControl.all[ Index ];
					if( EubIapCommonGetFieldType( ChildControl ) == "checkbox" )
					{
						if( ChildControl.checked )
							sField = iif( ( EubIapCommonIsBlank( sField ) ), sField, sField + ',' ) + oControl.all[ Index + 1 ].outerText;
					}
				}
				break;
			case "SqlValueDatePicker":
				sField = SqlValueDatePickerGetValueById( control );
				break;
			default:
				sField = oControl.value;
				break;
		}	
	}
	else if( property.toUpperCase() == "TEXT" )
	{
		switch( EubIapCommonGetFieldType( oControl ) )
		{ 
			case "select-one"	:
			case "select-multiple" :
				if( oControl.selectedIndex > -1 )
					sField = oControl.options[ oControl.selectedIndex ].text;
				else
					sField = "";
				break;
			//todo add any other controls that use the Text property
			default:
				sField = "undefined";
				break;
		}
	}
	return sField;
}

// Returns true if control is a DatePickerControl
// the datePicker is rendered as a table
// which contains rows with children controls
// loop the table tree and find the textbox or img controls
// check the cssClassName, which is the only attribute unique to a 
// sqlvalueDatePicker
function EubIapCommonIsControlDatePicker( oControl )
{
	var iIndex;
	var oDatePicker = oControl;
	var sClassName = '';
	
	try
	{
		if( !EubIapCommonIsUndefined( oDatePicker.children[0].children[0].children[0].children[1]) )
		{
			do
			{	
				oDatePicker = oDatePicker.children[0].children[0].children[0].children[1];
				
				if( oDatePicker.className.indexOf('SqlValueDatePicker') >= 0) // == 'SqlValueDatePickerTextBox' )
					return true
			
			}while( EubIapCommonIsBlank( sClassName ) )
		}
	}
	catch(error)
	{	
		return false;
	}
	
	return false;
}

// Returns the given control field type
function EubIapCommonGetFieldType( oControl )
{
    var sType = '';
	var ChildControl;
	
	if( oControl == null )
	    return;
		
	if( EubIapCommonIsUndefined( oControl.type ) )
	{ 
		if( EubIapCommonIsControlDatePicker( oControl ) )
			sType = "SqlValueDatePicker";
		else if( EubIapCommonIsUndefined( oControl.children ) )
		{
			if( oControl.length >= 1 )
			{
				if( !EubIapCommonIsUndefined( oControl[ 1 ].type ) )
					sType = oControl[ 1 ].type;
			}
			
		}else
		{
			for( var Index = 0; Index < oControl.all.length; Index++ )
			{
				ChildControl = oControl.all[ Index ];
				if( !EubIapCommonIsUndefined( ChildControl.type ) )
					return ChildControl.type + "list";
					//we do return here to exit for
			}
		}
	}
	else
	{ 
		sType = oControl.type;
	}
	
	return sType;
}

//caches object references for faster access (document.all is slow)
____cache = {}
function EubIapCommonGetControl( fieldName )
{
 return ____cache[fieldName] || (____cache[fieldName]=document.all(fieldName));
}


// Returns the selected value of a Radio Button List
function EubIapCommonGetRadioVal( oControl )
{

	var sValue;
	var L = oControl.length;

	if( L > 0 ) 
	{
		for( var i = 0 ; i < L ; i++ )
		{
			if( oControl[ i ].checked )
			{	
				return EubIapValidationCBoolean( oControl[ i ].value );		
			}
		}
	}else
	{
		//this check is put in for a case where the object is not a radio button list  but a group of radio buttons
		// thus they will not be an array of objects
		if( oControl.checked )
			return true;
		else
			return "";
			
	}
	//if not selected, it is still undefined.
	return sValue;


}

// Sets the selected Value of a Radio Button List
function EubIapCommonSetRadioVal( oControl, value )
{
	try
	{
		var L = oControl.length;
		
		for( var i = 0; i < L; i++ )
		{
			if( oControl[ i ].value == value )
			{
				oControl[ i ].checked = true;
				return;
			}
		}
	}
	catch( error )
	{
		//put in a broken rule
	}
}

// Returns a given control's field name
function EubIapCommonGetFieldName( oControl )
{
	var sField = "";
	var sType = EubIapCommonGetFieldType( oControl );
	if( sType == 'radio' )
	{
		if( oControl.length > 0 )
			sField = oControl[ 0 ].name;
		else
			sField = oControl.name;
	}
	else
		sField = oControl.name;

	return sField;
}

// Clears the contents of a given control
function EubIapCommonClearFieldContents( p_oField )
{  
	var sType = EubIapCommonGetFieldType( p_oField );

	switch(sType)
	{  
		case "select-one" :
		case "select-multiple" :
			if( p_oField.size > 0 ) 
				clearListBox( p_oField ); // it is a listbox
			else
				p_oField.selectedIndex = 0; //it is a drop-down
			break;
		case "radio" :
			for(var iIndex =0; iIndex < p_oField.length; iIndex++)
				p_oField[iIndex].checked = false;
			break;
		case "checkbox":
			p_oField.checked = false;
			break;
		case "button":
			break;
		default :
			p_oField.value = "";
			break;
	}

}

// Checks if value is of undefined type
function EubIapCommonIsUndefined( p_sValue )
{
	if( typeof( p_sValue ) == "undefined" )
		return true;
	else
		return false;
}
// Checks if value is Numeric
function EubIapCommonIsNumeric( p_sValue )
{
	return !( isNaN( Number( p_sValue ) ) );
}

// Calculates the difference in time between dates
function EubIapCommonDateDiff( p_sDate, p_sCompareDate )
{
	var date = new Date( p_sDate );
	var dDate = date.getTime();
	var compareDate = new Date( p_sCompareDate );
	var dCompareDate = compareDate.getTime();
	
	var dDiff = Number(dDate) - Number(dCompareDate);
	
	var days = Math.floor(dDiff / (1000 * 60 * 60 * 24));

	return days;
	
}

// Performs Date Comparisons
function EubIapCommonIsDateEqualOrLessThan( p_sDate, p_sCompareDate )
{

	var date = new Date();
	var dateString = p_sDate;
	
	if( EubIapCommonIsBlank( p_sDate ) || EubIapCommonIsBlank( p_sCompareDate ) )
		return true;
   
   date.setDate( dateString.substring(0,2) );
   //Sets the month in the Date object (from 0-11. 0=January, 1=February)
   date.setMonth( Number( EubIapCommonGetMonthNumber( dateString.substring(3,6) ) ) -1 );
   date.setFullYear( dateString.substring(7,11) );
   
   var dateCompare = new Date();
   var dateCompareString = p_sCompareDate;
   
   dateCompare.setDate( dateCompareString.substring(0,2) );
   //Sets the month in the Date object (from 0-11. 0=January, 1=February)
   dateCompare.setMonth( Number( EubIapCommonGetMonthNumber( dateCompareString.substring(3,6) ) ) -1 );
   dateCompare.setFullYear( dateCompareString.substring(7,11) );

	var days = EubIapCommonDateDiff( date , dateCompare );
	
	if( days <= 0 )
		return true;
	else
		return false;
}

// Gets month numeric value based on the month short description 
function EubIapCommonGetMonthNumber( p_sMonth )
{	
	p_sMonth = p_sMonth.toUpperCase();
	
	switch(p_sMonth)
	{	case "JAN":
			return 1;
			break;
		case "FEB":
			return 2;
			break;
		case "MAR":
			return 3;
			break;
		case "APR":
			return 4;
			break;
		case "MAY":
			return 5;
			break;
		case "JUN":
			return 6;
			break;
		case "JUL":
			return 7;
			break;
		case "AUG":
			return 8;
			break;
		case "SEP":
			return 9;
			break;
		case "OCT":
			return 10;
			break;
		case "NOV":
			return 11;
			break;
		case "DEC":
			return 12;
			break;
	}

}

// Gets month short description based on the month numeric value
function EubIapCommonGetMonthName( p_iMonth )
{	switch(p_iMonth)
	{	case 1:
			return "JAN";
			break;
		case 2:
			return "FEB";
			break;
		case 3:
			return "MAR";
			break;
		case 4:
			return "APR";
			break;
		case 5:
			return "MAY";
			break;
		case 6:
			return "JUN";
			break;
		case 7:
			return "JUL";
			break;
		case 8:
			return "AUG";
			break;
		case 9:
			return "SEP";
			break;
		case 10:
			return "OCT";
			break;
		case 11:
			return "NOV";
			break;
		case 12:
			return "DEC";
			break;
	}
}

// Gets month numeric value based on the month 3 character short description
function EubIapCommonGetMonthNumber( p_sMonth )
{	
	switch(p_sMonth.toUpperCase())
	{	case "JAN":
			return 1;
			break;
		case "FEB":
			return 2;
			break;
		case "MAR":
			return 3;
			break;
		case "APR":
			return 4;
			break;
		case "MAY":
			return 5;
			break;
		case "JUN":
			return 6;
			break;
		case "JUL":
			return 7;
			break;
		case "AUG":
			return 8;
			break;
		case "SEP":
			return 9;
			break;
		case "OCT":
			return 10;
			break;
		case "NOV":
			return 11;
			break;
		case "DEC":
			return 12;
			break;
	}
}

function EubIapCommonGetDatePlusSixMonth( day, month, year )
{
	var gaMonthCnt = new Array(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	var gaMonthCntL = new Array(31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	var isLeap = ((year%4==0)&(year%100!=0))|(year%400==0);
	
	var calMonth = Number(month);
	var calDay = Number(day);
	var calYear = Number(year);
	
	if( month <= 6 )
		calMonth = Number(month) + 6;
	else
	{	calMonth = (Number(month) + 6) - 12;
		calYear = Number(year) + 1;
	}
	if( isLeap )
		calDay = gaMonthCntL[ calMonth - 1 ];
	else
		calDay = gaMonthCnt[ calMonth - 1 ];
		
	if( Number(calDay) >= Number(day) )
		calDay = day;
	
	return iif( calDay < 10, "0" + Number(calDay), calDay ) + "-" + EubIapCommonGetMonthName( calMonth ) + "-" + calYear;
}

/// Sets the value of a control based on the selected value of a dropdown control and
/// the respective ClientSide array
/// Need this functionality to display Lov values from the EubFramework on different controls
function EubIapCommonSetControlValueFromDropDown( ControlToRead, ControlToSet, ArrayName, StartAtZero )
{
	var oReadControl = EubIapCommonGetControl( ControlToRead );
	var oSetControl = EubIapCommonGetControl( ControlToSet );
	var iIndex;
	var Value;
	
	if( oReadControl == null )
		return;
		
	if( oSetControl == null )
		return;
	
		
	if( !EubIapCommonIsDropDown( oReadControl ) )
		return;
	
	if( StartAtZero == false )
		iIndex = oReadControl.selectedIndex;	
	else
		iIndex = oReadControl.selectedIndex - 1;
	
	//if nothing has been selected on ControlToRead - clear ControlToSet
	if( iIndex < 0 )
	{	if( EubIapCommonIsDropDown( oSetControl ) )
			EubIapCommonClearDropDown( oSetControl );
		else
			EubIapCommonClearFieldContents( oSetControl );
		return;
	}
	
	Value =  eval( ArrayName + "[" + iIndex + "]" );
	
	if( EubIapCommonIsUndefined( Value ) )
		return;
	else
	{
		if( EubIapCommonIsDropDown( oSetControl ) )		
			EubIapCommonPopulateDropDown( oSetControl, Value );
		else
			oSetControl.value = decodeURI( Value );
			
	}
}
/// Sets the value of a control based on the selected value of a dropdown control and
/// the respective ClientSide array
/// Need this functionality to display Lov values from the EubFramework on different controls
function EubIapCommonSetControlValueFromCheckBox( ControlToRead, ControlToSet, ObjectName )
{
	var oReadControl = EubIapCommonGetControl( ControlToRead );
	var oSetControl = EubIapCommonGetControl( ControlToSet );
	
	if(oReadControl.checked)
	{		
		var value = this[ObjectName][oReadControl.parentNode.CheckBoxValue];
		oSetControl.value = decodeURI(value);
	} else
	{
		EubIapCommonClearFieldContents( oSetControl );
	}
}
var __rdoSet={};
var __rdoRead={};

function EubIapCommonSetControlValueFromRadioButton( ControlToRead, ControlToSet, ObjectName )
{
	var oReadControl = EubIapCommonGetControl( ControlToRead );	
	var oSetControl = EubIapCommonGetControl( ControlToSet );
	
	var name = oReadControl.name;
	
	if(typeof __rdoSet[name] != 'undefined')
	{
		EubIapCommonClearFieldContents(__rdoSet[name]);
	}
	__rdoSet[name] = oSetControl;
	
	var value = this[ObjectName][oReadControl.value];
	oSetControl.value = decodeURI(value);	
}
// Rounds the value to the p_dDimention decimals precision
function EubIapRoundValue(p_dValue, p_dDimention)
{  
	var vDecimals = '1';
	var iIndex;
	for(iIndex =0; iIndex < p_dDimention; iIndex++)
		vDecimals = vDecimals + '0';
	return Math.round(p_dValue * parseInt(vDecimals))/parseInt(vDecimals);
}

// Determines if a control is a single-select / multi-select drop down list
function EubIapCommonIsDropDown( Control )
{
	if( EubIapCommonGetFieldType( Control ) == "select-one" || EubIapCommonGetFieldType( Control ) == "select-multiple" )
		return true;
	else
		return false;
	
}

// Returns an array of values based upon the selected index of the drop down list
function EubIapCommonFilterArrayFromDropDown( ControlToRead, ArrayName )
{
	var oReadControl = EubIapCommonGetControl( ControlToRead );
	var localArray;
	var iIndex;
	
	if( oReadControl == null )
		return;

	if( !EubIapCommonIsDropDown( oReadControl ) )
		return;
		
	iIndex = oReadControl.selectedIndex - 1;	
	
	if( iIndex < 0 )
		return;
		
	localArray = eval( ArrayName + "[" + iIndex + "]" );	
	
	if( EubIapCommonIsUndefined( localArray ) )
		return;
	else
		return localArray;
}

// Populates a drop down list from an array of values
function EubIapCommonPopulateDropDown( control, listOfValues )
{
	var oOption; 

	if( listOfValues.length <= 0 )
		return;
	
	EubIapCommonClearDropDown( control );
	
	for(var iIndex = 0; iIndex <= listOfValues.length - 1; iIndex++ )
	{	
		oOption = document.createElement("OPTION");
		control.options.add( oOption, iIndex );
		oOption.innerText = listOfValues[ iIndex ];
		oOption.value = listOfValues[ iIndex ];
	}

}

function EubIapCommonGetDropDownItemIndexByValue( control, itemValue )
{
    for( var iIndex = 0; iIndex < control.options.length - 1; iIndex++ )
    {
        if( control.options[ iIndex ].value == itemValue )
            return iIndex;
    }
    return -1;
}

//Inserts a new option into a drop down list
function EubIapCommonInsertDropDownItem( control, itemValue, itemText, index )
{
    var oOption = document.createElement("OPTION");
	oOption.innerText = itemText;
	oOption.value = itemValue;
	control.insertBefore( oOption, control.options[index] );

}

// Removes all the items in a drop down list
function EubIapCommonClearDropDown( control )
{
	while(control.options.length)
	{
		  control.options.remove(0);
	}

}
// Formats the phone number fields to (###) ###-####
function EubIapCommonFormatPhoneFax()
{	
	var oField = EubIapCommonGetEventControl();
	var sFieldValue = EubIapCommonGetFieldValue( EubIapCommonGetFieldName( oField ) ,"Value" );
	var iLength = Number(sFieldValue.length);
	
	if(!(event.keyCode >=48 && event.keyCode <=57))
	{	event.keyCode = 0;
		iLength = iLength -1;
	}
	if(iLength ==1)
		oField.value = "(" + sFieldValue;
	if(iLength == 4)
		oField.value = sFieldValue + ") ";
	if(iLength == 9)
		oField.value = sFieldValue + "-";
		
}

function EubIapCommonToUpper(controlName)
{
	var control = EubIapCommonGetControl(controlName);
	control.value = control.value.toUpperCase();
}

// Moves cursor to next field if user has entered the max number of characters for the field
function EubIapCommonMoveToNextControl( notNumeric )
{  var oField;
	var sNextField;
	var sFieldValue;
	var iLength;
	var iMaxLength;
	
	//get Event object
	oField = EubIapCommonGetEventControl();
	
	if(oField == null)
		return;
	else if( oField.readOnly || oField.disabled )
		return;
	else
		sFieldValue = EubIapCommonGetFieldValue( EubIapCommonGetFieldName( oField ) ,"Value" );
	
	iMaxLength = oField.maxLength;
	// We need the - 1 because numeric fields have a buffer of 1 for +/- indicators
	if( !( notNumeric == true ) )
		iMaxLength--;
	
	//if field has reached Max - reset and continue
	if( Number(sFieldValue.length) == iMaxLength )
		oField.value = "";
			
	if(event.keyCode != 8 && event.keyCode !=46)
		iLength = Number(sFieldValue.length) + 1
	else
		iLength = Number(sFieldValue.length) -1
	
	if( iLength == iMaxLength )
	{	//commit onkeypress 
		//oField.value = sFieldValue + String.fromCharCode(event.keyCode);
	    sNextField = EubIapCommonGetNthControlName(EubIapCommonGetControlIndex(oField) +1);
		//goto next field
		setTimeout( "EubIapCommonGetControl( '" + sNextField + "' ).focus();",100 );
		 
	}
}

// Returns the event field object if there is one If no event was triggered, returns null
function EubIapCommonGetEventControl()
{	
	{	if(event == null)
			return null;
		else 
			return event.target;
	}
	//if(event == null)
	//		return null;
	//	else
	//		return event.srcElement;
}

// Returns the n index form field object
function EubIapCommonGetNthControlName(p_iIndex)
{  
	var a_oFields = document.forms[0].elements;
	
	return a_oFields[p_iIndex].name;
      
}

// Gets the field Index
function EubIapCommonGetControlIndex(p_oField) 
{	
	for (var i=0;document.forms[0].elements.length;i++)
	{	
		if (p_oField == document.forms[0].elements[i])
			return i;
	}
			
    return -1;
}

// Returns the row when the column name and value match
function EubIapCommonGetDataGridRowByColumnNameAndValue( datagrid, column, value )
{
	var dgControl = EubIapCommonGetControl( datagrid );
	var iCol = -1;
	var iRow;
	var iIndex = 0;
	
	do
	{
		if( dgControl.rows[ 0 ].cells[ iIndex ].innerText == column )
			iCol = iIndex;
		iIndex++;
	
	}while( iCol == -1 )
	
	if( iCol == -1 )
		return null;
	
	for( iIndex = 1; iIndex < dgControl.rows.length; iIndex++ )
	{
		if( dgControl.rows[ iIndex ].cells[ iCol ].innerText == value )
			return iIndex;
	}
	return -1;
}

// Returns the caption for a checkbox control
function EubIapCommonGetCheckBoxCaption( controlName )
{
	var Control = EubIapCommonGetControl( controlName );
	
	if( Control == null )
		return;
		
	return Control.parentNode.children[ 1 ].innerHTML;

}

// Compares two arrays elements lists and returns true if all elements are the same
function EubIapCommonCompareArrays( Array1, Array2 )
{
	if( Array1.length != Array2.length )
		return false;
	
	for( var Index = 0; Index < Array1.length; Index++ )
	{
		if( Array1[ Index ] != Array2[ Index ] )
			return false;
	}
	return true;
}

// Clears the client-side contents of a Datagrid control
function EubIapCommonClearDataGrid( datagridName )
{
	var Index;
	var Cnt;
	var datagrid = EubIapCommonGetControl( datagridName );
	var cell;
	
	if( datagrid == null )
		return;
	
	for( Index = 1; Index < datagrid.rows.length; Index++ )
	{
		for( Cnt = 0; Cnt < datagrid.rows[ Index ].cells.length; Cnt++ )
		{	cell = datagrid.rows[ Index ].cells[ Cnt ];
			if( cell.children.length > 0 )
			{
				if( cell.children[ 0 ].type == "submit" )
					cell.children[ 0 ].disabled = true;
			}else
				cell.innerText = "";		
		}
	}
}

// Scrolls the Menu frame
function resizeMenu()
{
	var oMenuFrame = EubIapCommonGetMenuFrame();
	
	oMenuFrame.document.body.scrollLeft = window.document.body.scrollLeft;
}

// Returns true if the function is called
function EubIapCommonIsPageLoaded()
{
	return true;
}

//This js function will find the index of an array element with the given value in an array.
//Usage: 
//var mnuArray = new Array(”Groups”,”Services”,”Applications”);
//mnuArray.findIndex(”Services”); - will return "1"
Array.prototype.findIndex = function(value){
    for (var i=0; i < this.length; i++) {
        // use === to check for Matches. ie., identical (===), ;
        if (this[i] == value) {
            return i;
        }
    }
    return -1;
};

//Returns a comma delimited string from all values of a given
//datagrid control column number
function EubIapCommonGetColumnCsvValuesFromDataGrid( datagridName, cellNumber )
{
    var datagrid = EubIapCommonGetControl( datagridName );
    var cnt = 1;
	var cellValue = '';
	var columnCSV = '';
   
   //create string of existing ba codes and companies
   //Start at 1 because first rows are headers
    for( cnt=1;cnt<datagrid.rows.length;cnt=cnt+1 )
    {
        cellValue = datagrid.rows[ cnt ].cells[ cellNumber ].innerText;
        if( !EubIapCommonIsBlank( cellValue ) )
            columnCSV = columnCSV + cellValue + ',';
    }
    
    return columnCSV;
}

/*
This function checks if a datagrid is empty
ASSUMPTIONS:
1) The datagrid is used in an updatePanel and has the following default setup:
    - First row is always the header
    - First cell is always the View Button
    - Second cell is always the Delete Button
2) Since it can be used after an asynchrounous post back, it needs to get a handle
   to the datagrid object usint $get - otherwise old values would still appear.
*/
function EubIapCommonIsUpdateSqlDataGridEmpty( gridName )
{
	var dataGrid = $get( gridName );
	
	//first row is header
	for(i = 1; i < dataGrid.rows.length; i = i + 1 )
	{   
	    //first two cells are buttons 
	    for(j = 2; j < dataGrid.rows[ i ].cells.length; j = j + 1 )
	    {
	        if( !EubIapCommonIsBlank( dataGrid.rows[ i ].cells[ j ].innerText ) )
	            return false;
	    }
	}

    return true;
}
///<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
/// End EubIapCommon Functionality 
///*********************************************************************************************
///*********************************************************************************************

-->