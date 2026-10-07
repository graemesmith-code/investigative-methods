<!--

/// ***********************************************************************************
/// ** REVISION HISTORY
/// ***********************************************************************************
/// ** Revision Date		Author			Comments
/// ** --------------------------------------------------------------------------------
/// ** 03/02/2006			D. Scholz		Converged the Page/framework template javascript into one
///	**										library, which includes the EubIapPageTemplate.js and EubIapEubFrameworkTemplate.js.
/// ***********************************************************************************

/// ----------------------------------------------------------------------------------
/// Global Variable Declarations
/// ----------------------------------------------------------------------------------

// stores a handle to the progress monitor iframe
var _EubIapPageProgressMonitor;

var _EubIapMvcTemplateTimer;

// stores a reference to a hidden field used for error messages
var _EubIapPageClientSideErrorMessage;

// stores a reference to a hidden field used to post transfer locations
var _EubIapPageTranferLocation;

// stores a field name to be set focus after the progress indicator has been disabled
var _EubIapPageControlToFocus = "";

//
var _EubIapPageIsIe6Up = true;

//
var _EubIapPageIsNav6Up = false;

//
var _EubIapPageWelpWindow;

// stores a handle to the ScheduleValidIndicator text box
var _ScheduleValidInd;

//
var _EubIapValidationDataTypeViolationsPresent;

//
var _DataViolationControl = null;

//variable used to close modal windows after a post back
//used after saves
var EubIapCloseModalWindow;

//variable used for UpdatePanels - AJAX
var _childUpdatePanelPostBack = false;

//Placeholder for pages that do not have
//grouped mappings
//All these variables are declared through the Class MvcAsyncPostBackUtility
//for pages using AsynPostBacks and grouped validations
var _EubIapValidationGroupLabels;
var _EubIapValidationGroupName;
var _EubIapGroupValidInd;

/// *********************************************************************************************
/// *********************************************************************************************
/// EubIapMvcTemplate Functionality
/// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

function EubIapMvcTemplateSetup()
{	

	/// Sets the global objects
	EubIapPageSetGlobalObjects();
	
	/// Enable the progress Monitor
	EubIapPageEnableProgressMonitor();	
	
	EubIapCommonDefaultSetup(); 
	
	EubIapPageDefaultSetup(); 
	
	EubIapEubFrameworkDefaultSetup();

	/// Enable the progress Monitor
	//EubIapPageDisableProgressMonitor();	
	_EubIapMvcTemplateTimer = setTimeout("EubIapPageDisableProgressMonitor()", 1000);

	
}

function EubIapMvcTemplateGetUseProgressMonitor()
{
	return eval( document.getElementById("_EubIapPageUseProgressMonitor").value );
	
}

/// *********************************************************************************************
/// *********************************************************************************************
/// EubIapPageTemplate Functionality 
/// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

//----------------------------------------------------------------------------------
// Exposed Properties
//----------------------------------------------------------------------------------

//saves the current Top scroll position of the page
function EubIapPageSaveScrollPosition()
{
	var scrollPosition = document.getElementById( "ScrollPositionOnPostBack" );
	
	if( scrollPosition != null )
		scrollPosition.value = document.body.scrollTop;
		
}

//saves the current Top scroll position of the page
function EubIapPageSetScrollPosition()
{
	var scrollPosition = document.getElementById( "ScrollPositionOnPostBack" );
	var top;
	
	if( EubIapCloseModalWindow == true )
		this.close();
	
	if( scrollPosition != null )
	{	top = scrollPosition.value;
		document.body.scrollTop = Number( top );
	}
		
}

// location - the location to transfer to
function EubIapPageTransferToLocation(location)
{
	var transfer = "" + location;

	if (transfer.length > 0)
	{
		__doPostBack("_EubIapPageClientSideTransferToButton", location);
	}		
}

function EubIapPageEnableProgressMonitorForHrefTransfer()
{
	EubIapPageEnableProgressMonitor();
	EubIapPageEnableControlsForPostBack();
	EubIapPageEncodeTextControls();
}

// Returns a handle to the progress monitor
function EubIapPageGetProgressMonitor()
{
	return _EubIapPageProgressMonitor;
}

function EubIapPageSetError(error)
{	
	_EubIapPageClientSideErrorMessage.Value = encodeURI(error);	
}

// Sets up any global object references used in this script
function EubIapPageSetGlobalObjects()
{
	_EubIapPageProgressMonitor = document.getElementById("_EubIapPageProgressMonitor");	
	_EubIapPageClientSideErrorMessage = document.getElementById("_EubIapPageClientSideErrorMessage");
}

// Sets up (positions) any page template objects
function EubIapPageSetObjectPositions()
{
	EubIapPageSetProgressMonitorPosition();
}

function EubIapPageSetProgressMonitorPosition()
{
	EubIapCommonSetScreenSize();
	_EubIapPageProgressMonitor.style.top = Math.round(EubIapCommonGetScreenHeight() / 2) - (60 / 2);
	_EubIapPageProgressMonitor.style.left = Math.round(EubIapCommonGetScreenWidth() / 2) - (150 / 2);

}

// Returns a boolean indicating if Client Browser is Ie 6+
function EubIapPageGetIsIe6Up()
{
	return _EubIapPageIsIe6Up;
}

// Returns a boolean indicating if Client Browser is Netscape 6+
function EubIapPageGetIsNav6Up()
{	
	return _EubIapPageIsNav6Up;	
}

// Encodes all of the sql value text controls
function EubIapPageEncodeTextControls()
{
	if (typeof(_TextControls) != "undefined")
	{
		for (controlIndex=0;controlIndex<_TextControls.length;controlIndex++)
		{
			if(_TextControls[controlIndex] != null)
			{
				/// TODO ==> WRAP THIS WITH MILLER'S FUNCTION
				_TextControls[controlIndex].value = encodeURI(_TextControls[controlIndex].value)
//				alert(_TextControls[controlIndex].value);
			}
		}
	}
}

// TODO ==> Move this into EubFramework.js
// Decodes all the custom SqlValue text controls
function EubIapPageDecodeTextControls()
{
	if (typeof(_TextControls) != "undefined")
	{
		for (controlIndex=0;controlIndex<_TextControls.length;controlIndex++)
		{
			if(_TextControls[controlIndex] != null)
			{
				/// TODO ==> WRAP THIS WITH MILLER'S FUNCTION
				_TextControls[controlIndex].value = decodeURI(_TextControls[controlIndex].value);
			}
		}
		clearTimeout( _EubIapMvcTemplateTimer );
	}
}

// Shows the working indicator
function EubIapPageEnableProgressMonitor() 
{
	if( !EubIapMvcTemplateGetUseProgressMonitor() )
		return;
		
	EubIapPageSetProgressMonitorPosition();
	this.EubIapCommonGetMainForm().style.display = "none";
	_EubIapPageProgressMonitor.style.display = "";	
}

// Hides the working indicator
function EubIapPageDisableProgressMonitor() 
{
	this.EubIapCommonGetMainForm().style.display = "";	
	_EubIapPageProgressMonitor.style.display = "none";
	EubIapPageSetScrollPosition();
	EubIapPageSetFieldFocus();

}

// Standard default setup of every page.  Its purpose is to handle any default 
// initialization needed for all pages, such as displaying server-side posted messages.
function EubIapPageDefaultSetup() 
{
	/// Checks and set Browser version variables
	EubIapPageSetBrowserVersion();
	
	/// Decode all of the text controls
	EubIapPageDecodeTextControls();

	/// Sets up the object positions	
	EubIapPageSetObjectPositions();
	
}

// Manages the control and display of server or client side errors.
// errorMessage - Message detailing the error.
// errorUrl - URL where the error occurred.
// errorLineNumber - Line where the error occurred.
function EubIapPagePostErrors(errorMessage, errorUrl, errorLineNumber) 
{
	if (typeof(errorMessage) != "undefined")
	{
		var message = "The following information has been gathered about the error: \n\n";
			message += "Message: " + errorMessage + "\n";
			message += "URL: " + errorUrl + "\n";
			message += "Line: " + errorLineNumber;
			alert(message);
			EubIapPageSetError(message);
		
			__doPostBack('_EubIapPageClientSideErrorButton','');			
	}		
	return true;
}

// Loads the Help Window
function EubIapPageLoadHelp( helpURL )
{
	//KDF - EubIapEasApplicationTemplate.js, EubIapEasAttachments.js, EubIapMvcWebTemplate.js and the stub menus is where this is hardcoded
	_EubIapPageWelpWindow = window.open('/eas.net/webhelp/EASUser.htm#' + helpURL,'EASHelp', 'width=600,height=405,top=0,left=50,toolbar=1,resizable=1,scrollbars=1, statusbar=1, status=1, menubar=1, location=1','EASHelp'); 
	_EubIapPageWelpWindow.location.reload();
	_EubIapPageWelpWindow.focus();
}

// A utility function determines if the client's browser is either Internet Explorer 6 + 
// or Navigator 6 +. If browser is neither - prompt user and redirect to main page
function EubIapPageSetBrowserVersion()
{	
	var agt=navigator.userAgent.toLowerCase();
	var is_nav  = ((agt.indexOf('mozilla')!=-1) && (agt.indexOf('spoofer')==-1)
      && (agt.indexOf('compatible') == -1) && (agt.indexOf('opera')==-1)
      && (agt.indexOf('webtv')==-1) && (agt.indexOf('hotjava')==-1));
	var is_ie     = ((agt.indexOf("msie") != -1) && (agt.indexOf("opera") == -1));

	var is_major = parseInt(navigator.appVersion);
	var is_minor = parseFloat(navigator.appVersion);
	var is_ie3    = (is_ie && (is_major < 4));
	var is_ie4    = (is_ie && (is_major == 4) && (agt.indexOf("msie 4")!=-1) );
	var is_ie4up  = (is_ie && (is_major >= 4));
	var is_ie5    = (is_ie && (is_major == 4) && (agt.indexOf("msie 5.0")!=-1) );
	var is_ie5_5  = (is_ie && (is_major == 4) && (agt.indexOf("msie 5.5") !=-1));
	var is_ie5up  = (is_ie && !is_ie3 && !is_ie4);
	var is_ie5_5up =(is_ie && !is_ie3 && !is_ie4 && !is_ie5);
	var is_ie6    = (is_ie && (is_major == 4) && (agt.indexOf("msie 6.")!=-1) );
		_EubIapPageIsIe6Up  = (is_ie && !is_ie3 && !is_ie4 && !is_ie5 && !is_ie5_5);
		_EubIapPageIsNav6Up = (is_nav && (is_major >= 5));
}

// Sets all radio buttons and dropdowns to disabled = false
// if the field is disabled, it does not post back the data
function EubIapPageEnableControlsForPostBack()
{
	var Index;
	var FieldName;
	var Control;

	for( Index=0; Index < _EubIapMainForm.length; Index++)
	{  
		FieldName = EubIapCommonGetNthControlName( Index );
		Control = EubIapCommonGetControl( FieldName );
		if( Control != null )
		{
			switch( EubIapCommonGetFieldType( Control ) )
			{
				case "radio":
					for( var i = 0; i < Control.length; i++ )
						Control[ i ].disabled = false;
					break;
				case "select-one":
				case "select-multiple" :
					Control.disabled = false;
					break;
			}

		}
	}

}

function EubIapPageSetControlToFocus( name )
{
	_EubIapPageControlToFocus = name;
}

function EubIapPageGetControlToFocus()
{
	return _EubIapPageControlToFocus;
}

function EubIapPageSetFieldFocus()
{
	var control;
	
	if( _EubIapPageControlToFocus == "" )
		return;
		
	control = EubIapCommonGetControl( _EubIapPageControlToFocus );
	
	if( control != null )
		control.focus();
	
}

/// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
/// End EubIapPageTemplate Functionality 
/// *********************************************************************************************
/// *********************************************************************************************



/// *********************************************************************************************
/// *********************************************************************************************
/// EubIapEubFrameworkTemplate Functionality 
/// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

// Resets the text and the css class of all labels associated with controls
function EubIapEubFrameworkResetControlLabels()
{
	if (typeof(_ControlLabels) != "undefined")
	{
		for (controlIndex=0;controlIndex<_ControlLabels.length;controlIndex++)
		{
			if(_ControlLabels[controlIndex] != null)
			{
				if (_ControlLabels[controlIndex].tag != "Ignore") //put in exclusion for controls not being validated by the framework
				{
				if (_ControlLabels[controlIndex].tag != "Ignore") //put in exclusion for controls not being validated by the framework
				{
					// reset the title (tooltip)
					_ControlLabels[controlIndex].title = "";			
					
					// undo the overriden color
					//_ControlLabels[controlIndex].style.color = "";
					var vCssNormal = _ControlLabels[controlIndex].getAttribute("CssDefault");
					if(vCssNormal != null)
						_ControlLabels[controlIndex].className = vCssNormal;
					else
						//This should never happen
						_ControlLabels[controlIndex].className = "";	
				}
				}
			}
		}
	}
}

// Returns the control associated with a ControlLabel
function EubIapEubFrameworkGetControlByLabelName( ControlLabel )
{
	var Controls = new Array();
	var controlIndex = 0;
	
	if( typeof(_ControlLabels) != "undefined" && typeof(_Controls) != "undefined" )
	{
		for( var Cnt=0; Cnt<_ControlLabels.length; Cnt++ )
		{
			if( _ControlLabels[ Cnt ].id == ControlLabel )
			{	Controls[ controlIndex ] = _Controls[ Cnt ];
				controlIndex = controlIndex + 1;
			}		
		}
	}
	return Controls;
}

// Sets up any global object references used in this script
function EubIapEubFrameworkSetGlobalObjects()
{
	_ScheduleValidInd = document.getElementById("ScheduleValidInd");
	if (_ScheduleValidInd != null && typeof(_ScheduleValidInd) != "undefined")	
		_ScheduleValidInd.disabled = false;
}

// Sets up any object positions.
function EubIapEubFrameworkSetObjectPositions()
{
}

//
function EubIapEubFrameworkPostErrorsToPage()
{
	/// TODO ==> Should probably check to see if the controls need to be enabled or not.
	/// First reset all of the control labels to a state not in error	
	EubIapEubFrameworkResetControlLabels();
	//need to re-evaluate the page in case another control affected the current datatype violation
	EubIapEubValidationValidateDataTypes();
	if (_EubIapValidationDataTypeViolations.length == 0)
	{
	    EubIapEubFrameworkPostBrokenRulesToPage();
	    _EubIapValidationDataTypeViolationsPresent = false;
	    _DataViolationControl = null;
	}
	else
	{		
		alert("The highlighted information is not valid.\nPlease re-enter ensuring the data type is right and the value is within the accepted range.\nThis field must be correctly entered before you can save.");

		_EubIapValidationDataTypeViolationsPresent = true;
		
		if (_ValidationRunIndicator)
			EubIapEubFrameworkPostDataTypeViolationsToPage();
		
		//reset the broken rules collection ...
		_EubIapValidationBrokenRules = null;
		_EubIapValidationBrokenRules = new Array();			
	}
}

//
function setFocus()
{
    if(_DataViolationControl) {
	    _DataViolationControl.focus();
	    _DataViolationControl.select();
	    _DataViolationControl = null;
    }
}

//
function EubIapEubFrameworkPostDataTypeViolationsToPage()
{	
	var brokenRule;
	if (typeof(_EubIapValidationDataTypeViolations) != "undefined")
	{
		var controlSet = false;
		for (ruleIndex=0; ruleIndex<_EubIapValidationDataTypeViolations.length; ruleIndex++)
		{
			brokenRule = _EubIapValidationDataTypeViolations[ ruleIndex ];
//			brokenRule = _EubIapValidationDataTypeViolations[ 0 ];
			
			if (brokenRule != null)
			{
				var label = null;
				label = document.getElementById(brokenRule.label);
				
				if (controlSet == false)
				{
					_DataViolationControl = document.getElementById(brokenRule.control);
					controlSet = true;
					setTimeout("setFocus()",100);
				}
				
				if (label != null)
				{
					var tooltip = "" + label.title;
					
					if (tooltip.length > 0)
						label.title = label.title + "\n" + brokenRule.message;
					else
						label.title = brokenRule.message;	
						
					//Changed to use the CssBrokenRule style instead of the cssDataTypeViolation -DS
					var vCssBrokenRule = label.getAttribute("CssBrokenRule");
					if(vCssBrokenRule != null)
						label.className = vCssBrokenRule;					
				}
			}
		}							
	}	
	_ValidationRunIndicator = false;
}

// Posts any of the broken rule messages to the correct label as tooltips
function EubIapEubFrameworkPostBrokenRulesToPage()
{
	//assume true until at least one brokenrule is added.
    //Innocent until proven guilty ;-)
	EubIapValidationSetScheduleValidInd(true);
    EubIapValidationResetGroupValidInd();
	
	if (typeof(_EubIapValidationBrokenRules) != "undefined")
	{
		for (ruleIndex=0; ruleIndex<_EubIapValidationBrokenRules.length; ruleIndex++)
		{
			brokenRule = _EubIapValidationBrokenRules[ ruleIndex ];
			
			if (brokenRule != null)
			{
				var label = null;
				label = document.getElementById(brokenRule.label);
				if (label != null)
				{
					var tooltip = "" + label.title;
					
					//KDF 4 CP - why do we unset the broken rule and the tooltip if the field
					//already has 1 broken rule message?
					//I'm commenting this out and hopefully not completely breaking something else.
					if (tooltip.length > 0)
					{
						var vCssBrokenRule = label.getAttribute("CssBrokenRule");
						if (label.className == vCssBrokenRule)
						{
							tooltip = "";
							var vCssNormal = label.getAttribute("CssDefault");
							if(vCssNormal != null)
								label.className = vCssNormal;
						}
					}
					
					if (tooltip.length > 0)
					{	if( label.title.indexOf( brokenRule.message ) == -1 )
							label.title = label.title + "\n" + brokenRule.message;
					}else
						label.title = brokenRule.message;	

					//Changed to use the CssBrokenRule style instead of the cssDataTypeViolation -DS
					var vCssBrokenRule = label.getAttribute("CssBrokenRule");
					if(vCssBrokenRule != null)
						label.className = vCssBrokenRule;
						
					EubIapValidationSetScheduleValidInd(false);
					
					//var _EubIapValidationGroupLabels is declared through the Class MvcAsyncPostBackUtility
					//for pages using AsynPostBacks and grouped validations
					if( !( EubIapCommonIsUndefined( _EubIapValidationGroupLabels  ) ) )
					{   
					    var groupName; 
					    
					    for( i=0; i < _EubIapValidationGroupName.length; i = i +1 )
					    {
					        groupName = _EubIapValidationGroupName[ i ];
    					    	
				            if( _EubIapValidationGroupLabels[ groupName ].findIndex( brokenRule.label ) > -1 )
				            {
				                EubIapValidationSetGroupValidInd( groupName, false );
				            }					    
					    
					    }
					}
					
				}
			}				
		}
	}	

	/// reset the rules collection
	_EubIapValidationBrokenRules = null;
	_EubIapValidationBrokenRules = new Array();	
}

// Returns the BrokenRule object array
function EubIapEubFrameworkGetBrokenRules()
{
	if (typeof(_EubIapValidationBrokenRules) != "undefined")
		return _EubIapValidationBrokenRules;
	else
		return null;
}

// Standard default setup of every page.  Its purpose is to handle any default 
// initialization needed for all pages, such as displaying server-side posted messages.
function EubIapEubFrameworkDefaultSetup() {

	/// Sets the global objects
	EubIapEubFrameworkSetGlobalObjects();
	
	/// Sets up the object positions	
	EubIapEubFrameworkSetObjectPositions();

	//EubIapEubValidationValidateDataTypes();
	
	///TODO rename this function
	validateLocal();	
	
	/// Process all of the errors
	EubIapEubFrameworkPostErrorsToPage();
	
}

//
function EubIapValidationIsPageValid()
{
	//var indicator = EubIapCommonGetFieldValue("_ScheduleValidInd", "Value").toUpperCase();
	//return (indicator == "TRUE");
	return _PageValidInd;
}		

function EubIapValidationIsGroupValid( groupName )
{
	return _EubIapGroupValidInd[ groupName ];
}	
//
function EubIapValidationDataTypeViolationsPresent()
{
	return _EubIapValidationDataTypeViolationsPresent;	
}

//
function EubIapValidationSetScheduleValidInd(isValid)
{
	_PageValidInd = isValid;
	
	try
	{
		if (_ScheduleValidInd != null && typeof(_ScheduleValidInd) != "undefined")	
		{
			if (isValid)			
				_ScheduleValidInd.value = "True";
			else
				_ScheduleValidInd.value = "False";	
		}
	}
	catch (error) {}
}

function EubIapValidationResetGroupValidInd()
{
 
    //var _EubIapValidationGroupLabels is declared through the Class MvcAsyncPostBackUtility
	//for pages using AsynPostBacks and grouped validations
	if( !( EubIapCommonIsUndefined( _EubIapValidationGroupLabels  ) ) )
	{   
	    var groupName; 
	    
	    for( i=0; i < _EubIapValidationGroupName.length; i = i +1 )
	    {
	        groupName = _EubIapValidationGroupName[ i ];
	        //first reset
	        //Innocent until proven guilty ;-)
	    	EubIapValidationSetGroupValidInd( groupName , true);
	    }
	}
}

//var _EubIapGroupValidInd is declared through the Class MvcAsyncPostBackUtility
//for pages using AsynPostBacks and grouped validations
function EubIapValidationSetGroupValidInd( groupName, isValid)
{
	_EubIapGroupValidInd[ groupName ] = isValid;

}

/// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
/// End EubIapEubFrameworkTemplate Functionality 
/// *********************************************************************************************
/// *********************************************************************************************

/// Set event handlers
window.onerror = EubIapPagePostErrors;

-->