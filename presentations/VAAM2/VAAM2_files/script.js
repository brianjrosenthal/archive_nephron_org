var CtxAlwaysOn = false;
function LoadSld( slideId )
{
	if( !g_supportsPPTHTML ) return
	if( slideId )
		parent.base.SldUpdated(slideId)
	g_origSz=parseInt(SlideObj.style.fontSize)
	g_origH=SlideObj.style.posHeight
	g_origW=SlideObj.style.posWidth
	g_scaleHyperlinks=(document.all.tags("AREA").length>0)
	if ( IsWin("PPTSld") && !parent.IsFullScrMode() )
		parent.base.highlite();	
	if( g_scaleHyperlinks )
		InitHLinkArray()
	if( g_scaleInFrame||(IsWin("PPTSld") && parent.IsFullScrMode() ) )
		document.body.scroll="no"
	_RSW()
	if( IsWin("PPTSld") && (parent.IsFullScrMode() || CtxAlwaysOn ) )	{
		document.oncontextmenu=parent._CM;
	self.focus(); 

	}
}
function MakeSldVis( fTrans ) 
{
	fTrans=fTrans && g_showAnimation
	if( fTrans )
	{
		if( g_bgSound ) {
			idx=g_bgSound.indexOf(",");
			pptSound.src=g_bgSound.substr( 0, idx );
			pptSound.loop= -(parseInt(g_bgSound.substr(idx+1)));
		}
		SlideObj.filters.revealtrans.Apply()
	}
	SlideObj.style.visibility="visible"
	if( fTrans )
		SlideObj.filters.revealtrans.Play()
}
function MakeNotesVis() 
{
	if( !IsNts() ) return false 
	SlideObj.style.display="none"
	nObj = document.all.item("NotesObj")
	parent.SetHasNts(0)
	if( nObj ) { 
		nObj.style.display=""
		parent.SetHasNts(1)
	}
	return 1
}
function Redirect( frmId,sId )
{
	var str=document.location.hash,idx=str.indexOf('#')
	if(idx>=0) str=str.substr(1);
	if( window.name != frmId && ( sId != str) ) {
		obj = document.all.item("Main-File")
		window.location.href=obj.href+"#"+sId
		return 1
	}
	return 0
}
function HideMenu() { if( frames["PPTSld"] && PPTSld.document.all.item("ctxtmenu") && PPTSld.ctxtmenu.style.display!="none" ) { PPTSld.ctxtmenu.style.display='none'; return true } return false }
function IsWin( name ) { return window.name == name }
function IsNts() { return IsWin("PPTNts") }
function IsSldOrNts() { return( IsWin("PPTSld")||IsWin("PPTNts") ) }
function SupportsPPTAnimation() { return( navigator.platform == "Win32" && navigator.appVersion.indexOf("Windows")>0 ) }
function SupportsPPTHTML()
{
	var appVer=navigator.appVersion, msie=appVer.indexOf( "MSIE " ), inex = appVer.indexOf( "Internet Explorer " ), ver=0
	if( msie >= 0 )
		ver=parseFloat( appVer.substring( msie+5, appVer.indexOf(";",msie) ) )
	else if( inex >= 0 )
		ver=parseFloat( appVer.substring( inex+18, appVer.indexOf(";",inex) ) )
	else
		ver=parseInt(appVer)

	return( ver >= 4  )
}
var MHTMLPrefix = CalculateMHTMLPrefix(); 
function CalculateMHTMLPrefix()
{
	if ( document.location.protocol == 'mhtml:') { 
		href=new String(document.location.href) 
		Start=href.indexOf('!')+1 
		End=href.lastIndexOf('/')+1 
		if (End < Start) 
			return href.substring(0, Start) 
		else 
		return href.substring(0, End) 
	}
	return '';
}

function LoadNavSld(slideId) {
playList();
parent.createCM();
	if( !g_supportsPPTHTML ) return
	if( IsWin("PPTSld") && slideId )
		parent.base.SldUpdated(slideId)
	self.focus(); 

}
var hasNarration = false;
function _RSW()
{
	if( !g_supportsPPTHTML || IsNts() ||
	  ( !g_scaleInFrame && (( window.name != "PPTSld" ) ) ) )
		return

	cltWidth=document.body.clientWidth
	cltHeight=document.body.clientHeight
	factor=(1.0*cltWidth)/g_origW
	if( cltHeight < g_origH*factor )
		factor=(1.0*cltHeight)/g_origH

	newSize = g_origSz * factor
	if( newSize < 1 ) newSize=1

	s=SlideObj.style
	s.fontSize=newSize+"px"
	s.posWidth=g_origW*factor
	s.posHeight=g_origH*factor
	s.posLeft=(cltWidth-s.posWidth)/2
	s.posTop=(cltHeight-s.posHeight)/2

	if ( hasNarration ) {
		obj = document.all.NSPlay.style;
		mySld = document.all.SlideObj.style;
		obj.position = 'absolute';
		obj.posTop = mySld.posTop + mySld.posHeight - 20;
		obj.posLeft = mySld.posLeft + mySld.posWidth - 20;
	}
	if( g_scaleHyperlinks )
		ScaleHyperlinks( factor );	
}
function IsMac() {
	return (window.navigator.platform.indexOf("Mac") >= 0 );
}

function HitOK( evt ) {
	//Nav Only function
	return (evt.which == 1 || (IsMac() && evt.which == 3) );
}
function _KPH(event)
{ 

  if ( parent.base.msie < 0 )  {
    
    	if ( ( (event.target.name && event.target.name == "hasMap" ) || (event.target.href && event.target.href != "") ) && parent.g_docTable[0].type != "jpeg" && HitOK( event )  ) {
    		return; /* to make hyperlinks in fullscreen mode traversable */
    	}
	if( IsContextMenu() )
		return parent.KPH(event);
  	if ( parent.IsFullScrMode()  && event.which == 27 )
  		parent.base.CloseFullScreen();
  	else if ( parent.base.IsFullScrMode() && ( (!IsMac() && event.which == 3) || ( IsMac() && (event.modifiers & Event.CONTROL_MASK) && event.which == 1 ) ) )
  		return parent.KPH(event);
  	else if( (event.which == 32) ||  (event.which == 13) || HitOK( event )  ) {
	    if( window.name == "PPTSld" )
	      parent.PPTSld.DocumentOnClick();
	    else
	      parent.M_GoNextSld();
      }	
      else if ( parent.IsFullScrMode() && ((event.which == 78)  || (event.which == 110) || (event.which == 29) || (event.which == 31) || (event.which == 12)) )
  		parent.M_GoNextSld();
      else if ( parent.IsFullScrMode() && ( (event.which == 80)  || (event.which == 112) || (event.which == 30) || (event.which == 28) || (event.which == 11) || (event.which == 8)) )
  		parent.M_GoPrevSld();

      return;
   }
  	
  if( IsNts() ) return;

  if(parent.IsFullScrMode()  && event.keyCode == 27 && !parent.HideMenu() )
    parent.base.CloseFullScreen();
  else if( (event.keyCode == 32) || (event.keyCode == 13) )
  {
    if( window.name == "PPTSld" )
      parent.PPTSld.DocumentOnClick();
   else
      parent.M_GoNextSld();
  }
  else if ( parent.IsFullScrMode() && ((event.keyCode == 78)  || (event.keyCode == 110)) )
  	parent.M_GoNextSld();
  else if ( parent.IsFullScrMode() && ((event.keyCode == 80)  || (event.keyCode == 112)) )
  	parent.M_GoPrevSld();
}

function DocumentOnClick(event)
{
		if ( g_doAdvOnClick && !parent.IsFullScrMode() ) {
			parent.base.TP_GoToNextSld();	
			return;
		}
		
	if ( parent.base.msie < 0 ) 
	{
		if( ( g_allowAdvOnClick  && parent.IsFullScrMode() ) || g_doAdvOnClick ||
		    (event && ( (event.which == 32) || (event.which == 13) ) ) )
			parent.M_GoNextSld();
			return;
	}		
	if( IsNts() || (parent.IsFullScrMode() && parent.HideMenu() ) ) return;
	if( ( g_allowAdvOnClick && parent.IsFullScrMode() ) || g_doAdvOnClick ||
	    (event && ( (event.keyCode==32) || (event.keyCode == 13) ) ) )
		parent.M_GoNextSld();
}


var g_supportsPPTHTML = SupportsPPTHTML(), g_scaleInFrame = true, gId="", g_bgSound="",
    g_scaleHyperlinks = false, g_allowAdvOnClick = true, g_showInBrowser = false, g_doAdvOnClick = false;

 var g_showAnimation = 0;
var g_hasTrans = false, g_autoTrans = false, g_transSecs = 0;
var g_isKiosk = 0;
var g_animManager = null;

var ENDSHOW_MESG="End of slide show, click to exit.", SCREEN_MODE="Frames", gIsEndShow=0, NUM_VIS_SLDS=270, SCRIPT_HREF="script.js", FULLSCR_HREF="fullscreen.htm";
var gCurSld = gPrevSld = 1, g_offset = 0, gNtsOpen = gHasNts = gOtlTxtExp = gNarrationPaused = false, gOtlOpen = true
window.gPPTHTML=SupportsPPTHTML()
var g_hideNav = 0;
function UpdNtsPane(){ PPTNts.location.replace( MHTMLPrefix+GetHrefObj( gCurSld ).mNtsHref ) }
function UpdNavPane( sldIndex ){ if(gNavLoaded) PPTNav.UpdNav() }
function UpdOtNavPane(){ if(gOtlNavLoaded) PPTOtlNav.UpdOtlNav() }
function UpdOtlPane(){ if(gOtlLoaded) PPTOtl.UpdOtl() }
function SetHasNts( fVal )
{
	if( gHasNts != fVal ) {
		gHasNts=fVal
		UpdNavPane()
	}
}

function ToggleVNarration()
{
	if ( base.msie < 0 ) {
		PPTSld.ToggleSound( false, PPTSld.document.NSPlay );
		return;
	}
	
	rObj=PPTSld.document.all("NSPlay")
	if( rObj ) {
		if( gNarrationPaused )
			rObj.Play()
		else
			rObj.Pause()

		gNarrationPaused=!gNarrationPaused
	}
}

function PrevSldViewed(){ GoToSld( GetHrefObj(gPrevSld).mSldHref ) }
function HasPrevSld() { return ( gIsEndShow || ( g_currentSlide != 1 && GetHrefObj( g_currentSlide-1 ).mVis == 1 )||( GetCurrentSlideNum() > 1 ) ) }
function HasNextSld() { return (GetCurrentSlideNum() != GetNumSlides()) }
function StartEndShow()
{
//	g_hideNav = 1;
//	PPTNav.location.reload();
	if( PPTSld.event ) PPTSld.event.cancelBubble=true

	doc=PPTSld.document
	doc.open()
	doc.writeln('<html><head><script > /*defer>*/ g_ctxmenu = 0; ' +
	'if( parent.base.msie < 0 )  { document.captureEvents(Event.KEYPRESS); document.captureEvents(Event.MOUSEDOWN); document.onkeypress = _KPH; document.onmousedown = _KPH; } ' +
	'function DocumentOnClick(event) { return _KPH(event); }  function IsContextMenu() { return (g_ctxmenu ==1); } ' +
	'function _KPH(event)' +
	'{  ' +
	'if ( parent.base.msie < 0  && (parent.IsFullScrMode() ) && event ) { if ( (!parent.IsMac() && event.which == 3) || ( parent.IsMac() && (event.modifiers & Event.CONTROL_MASK) && event.which == 1 ) )  { return parent.KPH(event); } ' + 
	' else if (event.which == 27 || event.which == 32 || event.which == 13 || parent.HitOK( event ) || (event.which == 78)  || (event.which == 110) || (event.which == 29) || (event.which == 31) || (event.which == 12) ) { if ( IsContextMenu() ) { return parent.KPH(event); }  parent.base.CloseFullScreen(); return; } ' +
	' else if ( (event.which == 80)  || (event.which == 112) || (event.which == 30) || (event.which == 28) || (event.which == 11) || (event.which == 8) ) { parent.M_GoPrevSld(); } } ' +
	'if( parent.HideMenu() ) return; if( (parent.IsFullScrMode() ) && event) { if ( (event.keyCode==27 || event.keyCode == 13 || event.keyCode==32 || event.type=="click" ) || (event.keyCode == 78)  || (event.keyCode == 110) ) { parent.base.CloseFullScreen(); }' +
	' else if ( (event.keyCode == 80)  || (event.keyCode == 112) ) { parent.M_GoPrevSld(); } } } function Unload() { parent.gIsEndShow=0; } function SetupEndShow() {    if ( !parent.IsFullScrMode() ) { return; } else { parent.PPTNav.location.reload(); }  parent.gIsEndShow=1; if ( parent.g_docTable[0].type != "jpeg" ) { if ( parent.base.msie < 0 ) {parent.createCM(); } document.oncontextmenu=parent._CM; } }</script></head><body scroll=\"no\" onclick=\"DocumentOnClick(event)\" onkeypress=\"_KPH(event)\" bgcolor=\"black\" onload=\"SetupEndShow()\" onunload=\"Unload()\"><center><p><font face=Tahoma color=white size=2><br><b>' + ENDSHOW_MESG + '</b></font></p></center></body></html>')
	doc.close()
}
function SetSldVisited(){ gDocTable[gCurSld-1].mVisited=true }
function IsSldVisited(){ return gDocTable[gCurSld-1].mVisited }
function hrefList( sldHref, visible, sldIdx )
{
	this.mSldHref= this.mNtsHref = sldHref
	this.mSldIdx = sldIdx
	this.mOrigVis= this.mVis = visible
	this.mVisited= false
}
var gDocTable = new Array(
   new hrefList("slide0541.htm", 1, 1),
   new hrefList("slide0542.htm", 1, 2),
   new hrefList("slide0543.htm", 1, 3),
   new hrefList("slide0544.htm", 1, 4),
   new hrefList("slide0545.htm", 1, 5),
   new hrefList("slide0546.htm", 1, 6),
   new hrefList("slide0547.htm", 1, 7),
   new hrefList("slide0548.htm", 1, 8),
   new hrefList("slide0549.htm", 1, 9),
   new hrefList("slide0550.htm", 1, 10),
   new hrefList("slide0551.htm", 1, 11),
   new hrefList("slide0552.htm", 1, 12),
   new hrefList("slide0553.htm", 1, 13),
   new hrefList("slide0554.htm", 1, 14),
   new hrefList("slide0555.htm", 1, 15),
   new hrefList("slide0556.htm", 1, 16),
   new hrefList("slide0557.htm", 1, 17),
   new hrefList("slide0558.htm", 1, 18),
   new hrefList("slide0559.htm", 1, 19),
   new hrefList("slide0560.htm", 1, 20),
   new hrefList("slide0561.htm", 1, 21),
   new hrefList("slide0562.htm", 1, 22),
   new hrefList("slide0563.htm", 1, 23),
   new hrefList("slide0564.htm", 1, 24),
   new hrefList("slide0565.htm", 1, 25),
   new hrefList("slide0566.htm", 1, 26),
   new hrefList("slide0567.htm", 1, 27),
   new hrefList("slide0568.htm", 1, 28),
   new hrefList("slide0569.htm", 1, 29),
   new hrefList("slide0570.htm", 1, 30),
   new hrefList("slide0571.htm", 1, 31),
   new hrefList("slide0572.htm", 1, 32),
   new hrefList("slide0573.htm", 1, 33),
   new hrefList("slide0574.htm", 1, 34),
   new hrefList("slide0575.htm", 1, 35),
   new hrefList("slide0576.htm", 1, 36),
   new hrefList("slide0577.htm", 1, 37),
   new hrefList("slide0578.htm", 1, 38),
   new hrefList("slide0579.htm", 1, 39),
   new hrefList("slide0580.htm", 1, 40),
   new hrefList("slide0581.htm", 1, 41),
   new hrefList("slide0582.htm", 1, 42),
   new hrefList("slide0583.htm", 1, 43),
   new hrefList("slide0584.htm", 1, 44),
   new hrefList("slide0585.htm", 1, 45),
   new hrefList("slide0586.htm", 1, 46),
   new hrefList("slide0587.htm", 1, 47),
   new hrefList("slide0588.htm", 1, 48),
   new hrefList("slide0589.htm", 1, 49),
   new hrefList("slide0590.htm", 1, 50),
   new hrefList("slide0591.htm", 1, 51),
   new hrefList("slide0592.htm", 1, 52),
   new hrefList("slide0593.htm", 1, 53),
   new hrefList("slide0594.htm", 1, 54),
   new hrefList("slide0595.htm", 1, 55),
   new hrefList("slide0596.htm", 1, 56),
   new hrefList("slide0597.htm", 1, 57),
   new hrefList("slide0598.htm", 1, 58),
   new hrefList("slide0599.htm", 1, 59),
   new hrefList("slide0600.htm", 1, 60),
   new hrefList("slide0601.htm", 1, 61),
   new hrefList("slide0602.htm", 1, 62),
   new hrefList("slide0603.htm", 1, 63),
   new hrefList("slide0604.htm", 1, 64),
   new hrefList("slide0605.htm", 1, 65),
   new hrefList("slide0606.htm", 1, 66),
   new hrefList("slide0607.htm", 1, 67),
   new hrefList("slide0608.htm", 1, 68),
   new hrefList("slide0609.htm", 1, 69),
   new hrefList("slide0610.htm", 1, 70),
   new hrefList("slide0611.htm", 1, 71),
   new hrefList("slide0612.htm", 1, 72),
   new hrefList("slide0613.htm", 1, 73),
   new hrefList("slide0614.htm", 1, 74),
   new hrefList("slide0615.htm", 1, 75),
   new hrefList("slide0616.htm", 1, 76),
   new hrefList("slide0617.htm", 1, 77),
   new hrefList("slide0618.htm", 1, 78),
   new hrefList("slide0619.htm", 1, 79),
   new hrefList("slide0620.htm", 1, 80),
   new hrefList("slide0621.htm", 1, 81),
   new hrefList("slide0622.htm", 1, 82),
   new hrefList("slide0623.htm", 1, 83),
   new hrefList("slide0624.htm", 1, 84),
   new hrefList("slide0625.htm", 1, 85),
   new hrefList("slide0626.htm", 1, 86),
   new hrefList("slide0627.htm", 1, 87),
   new hrefList("slide0628.htm", 1, 88),
   new hrefList("slide0629.htm", 1, 89),
   new hrefList("slide0630.htm", 1, 90),
   new hrefList("slide0631.htm", 1, 91),
   new hrefList("slide0632.htm", 1, 92),
   new hrefList("slide0633.htm", 1, 93),
   new hrefList("slide0634.htm", 1, 94),
   new hrefList("slide0635.htm", 1, 95),
   new hrefList("slide0636.htm", 1, 96),
   new hrefList("slide0637.htm", 1, 97),
   new hrefList("slide0638.htm", 1, 98),
   new hrefList("slide0639.htm", 1, 99),
   new hrefList("slide0640.htm", 1, 100),
   new hrefList("slide0641.htm", 1, 101),
   new hrefList("slide0642.htm", 1, 102),
   new hrefList("slide0643.htm", 1, 103),
   new hrefList("slide0644.htm", 1, 104),
   new hrefList("slide0645.htm", 1, 105),
   new hrefList("slide0646.htm", 1, 106),
   new hrefList("slide0647.htm", 1, 107),
   new hrefList("slide0648.htm", 1, 108),
   new hrefList("slide0649.htm", 1, 109),
   new hrefList("slide0650.htm", 1, 110),
   new hrefList("slide0651.htm", 1, 111),
   new hrefList("slide0652.htm", 1, 112),
   new hrefList("slide0653.htm", 1, 113),
   new hrefList("slide0654.htm", 1, 114),
   new hrefList("slide0655.htm", 1, 115),
   new hrefList("slide0656.htm", 1, 116),
   new hrefList("slide0657.htm", 1, 117),
   new hrefList("slide0658.htm", 1, 118),
   new hrefList("slide0659.htm", 1, 119),
   new hrefList("slide0660.htm", 1, 120),
   new hrefList("slide0661.htm", 1, 121),
   new hrefList("slide0662.htm", 1, 122),
   new hrefList("slide0663.htm", 1, 123),
   new hrefList("slide0664.htm", 1, 124),
   new hrefList("slide0665.htm", 1, 125),
   new hrefList("slide0666.htm", 1, 126),
   new hrefList("slide0667.htm", 1, 127),
   new hrefList("slide0668.htm", 1, 128),
   new hrefList("slide0669.htm", 1, 129),
   new hrefList("slide0670.htm", 1, 130),
   new hrefList("slide0671.htm", 1, 131),
   new hrefList("slide0672.htm", 1, 132),
   new hrefList("slide0673.htm", 1, 133),
   new hrefList("slide0674.htm", 1, 134),
   new hrefList("slide0675.htm", 1, 135),
   new hrefList("slide0676.htm", 1, 136),
   new hrefList("slide0677.htm", 1, 137),
   new hrefList("slide0678.htm", 1, 138),
   new hrefList("slide0679.htm", 1, 139),
   new hrefList("slide0680.htm", 1, 140),
   new hrefList("slide0681.htm", 1, 141),
   new hrefList("slide0682.htm", 1, 142),
   new hrefList("slide0683.htm", 1, 143),
   new hrefList("slide0684.htm", 1, 144),
   new hrefList("slide0685.htm", 1, 145),
   new hrefList("slide0686.htm", 1, 146),
   new hrefList("slide0687.htm", 1, 147),
   new hrefList("slide0688.htm", 1, 148),
   new hrefList("slide0689.htm", 1, 149),
   new hrefList("slide0690.htm", 1, 150),
   new hrefList("slide0691.htm", 1, 151),
   new hrefList("slide0692.htm", 1, 152),
   new hrefList("slide0693.htm", 1, 153),
   new hrefList("slide0694.htm", 1, 154),
   new hrefList("slide0695.htm", 1, 155),
   new hrefList("slide0696.htm", 1, 156),
   new hrefList("slide0697.htm", 1, 157),
   new hrefList("slide0698.htm", 1, 158),
   new hrefList("slide0699.htm", 1, 159),
   new hrefList("slide0700.htm", 1, 160),
   new hrefList("slide0701.htm", 1, 161),
   new hrefList("slide0702.htm", 1, 162),
   new hrefList("slide0703.htm", 1, 163),
   new hrefList("slide0704.htm", 1, 164),
   new hrefList("slide0705.htm", 1, 165),
   new hrefList("slide0706.htm", 1, 166),
   new hrefList("slide0707.htm", 1, 167),
   new hrefList("slide0708.htm", 1, 168),
   new hrefList("slide0709.htm", 1, 169),
   new hrefList("slide0710.htm", 1, 170),
   new hrefList("slide0711.htm", 1, 171),
   new hrefList("slide0712.htm", 1, 172),
   new hrefList("slide0713.htm", 1, 173),
   new hrefList("slide0714.htm", 1, 174),
   new hrefList("slide0715.htm", 1, 175),
   new hrefList("slide0716.htm", 1, 176),
   new hrefList("slide0717.htm", 1, 177),
   new hrefList("slide0718.htm", 1, 178),
   new hrefList("slide0719.htm", 1, 179),
   new hrefList("slide0720.htm", 1, 180),
   new hrefList("slide0721.htm", 1, 181),
   new hrefList("slide0722.htm", 1, 182),
   new hrefList("slide0723.htm", 1, 183),
   new hrefList("slide0724.htm", 1, 184),
   new hrefList("slide0725.htm", 1, 185),
   new hrefList("slide0726.htm", 1, 186),
   new hrefList("slide0727.htm", 1, 187),
   new hrefList("slide0728.htm", 1, 188),
   new hrefList("slide0729.htm", 1, 189),
   new hrefList("slide0730.htm", 1, 190),
   new hrefList("slide0731.htm", 1, 191),
   new hrefList("slide0732.htm", 1, 192),
   new hrefList("slide0733.htm", 1, 193),
   new hrefList("slide0734.htm", 1, 194),
   new hrefList("slide0735.htm", 1, 195),
   new hrefList("slide0736.htm", 1, 196),
   new hrefList("slide0737.htm", 1, 197),
   new hrefList("slide0738.htm", 1, 198),
   new hrefList("slide0739.htm", 1, 199),
   new hrefList("slide0740.htm", 1, 200),
   new hrefList("slide0741.htm", 1, 201),
   new hrefList("slide0742.htm", 1, 202),
   new hrefList("slide0743.htm", 1, 203),
   new hrefList("slide0744.htm", 1, 204),
   new hrefList("slide0745.htm", 1, 205),
   new hrefList("slide0746.htm", 1, 206),
   new hrefList("slide0747.htm", 1, 207),
   new hrefList("slide0748.htm", 1, 208),
   new hrefList("slide0749.htm", 1, 209),
   new hrefList("slide0750.htm", 1, 210),
   new hrefList("slide0751.htm", 1, 211),
   new hrefList("slide0752.htm", 1, 212),
   new hrefList("slide0753.htm", 1, 213),
   new hrefList("slide0754.htm", 1, 214),
   new hrefList("slide0755.htm", 1, 215),
   new hrefList("slide0756.htm", 1, 216),
   new hrefList("slide0757.htm", 1, 217),
   new hrefList("slide0758.htm", 1, 218),
   new hrefList("slide0759.htm", 1, 219),
   new hrefList("slide0760.htm", 1, 220),
   new hrefList("slide0761.htm", 1, 221),
   new hrefList("slide0762.htm", 1, 222),
   new hrefList("slide0763.htm", 1, 223),
   new hrefList("slide0764.htm", 1, 224),
   new hrefList("slide0765.htm", 1, 225),
   new hrefList("slide0766.htm", 1, 226),
   new hrefList("slide0767.htm", 1, 227),
   new hrefList("slide0768.htm", 1, 228),
   new hrefList("slide0769.htm", 1, 229),
   new hrefList("slide0770.htm", 1, 230),
   new hrefList("slide0771.htm", 1, 231),
   new hrefList("slide0772.htm", 1, 232),
   new hrefList("slide0773.htm", 1, 233),
   new hrefList("slide0774.htm", 1, 234),
   new hrefList("slide0775.htm", 1, 235),
   new hrefList("slide0776.htm", 1, 236),
   new hrefList("slide0777.htm", 1, 237),
   new hrefList("slide0778.htm", 1, 238),
   new hrefList("slide0779.htm", 1, 239),
   new hrefList("slide0780.htm", 1, 240),
   new hrefList("slide0781.htm", 1, 241),
   new hrefList("slide0782.htm", 1, 242),
   new hrefList("slide0783.htm", 1, 243),
   new hrefList("slide0784.htm", 1, 244),
   new hrefList("slide0785.htm", 1, 245),
   new hrefList("slide0786.htm", 1, 246),
   new hrefList("slide0787.htm", 1, 247),
   new hrefList("slide0788.htm", 1, 248),
   new hrefList("slide0789.htm", 1, 249),
   new hrefList("slide0790.htm", 1, 250),
   new hrefList("slide0791.htm", 1, 251),
   new hrefList("slide0792.htm", 1, 252),
   new hrefList("slide0793.htm", 1, 253),
   new hrefList("slide0794.htm", 1, 254),
   new hrefList("slide0795.htm", 1, 255),
   new hrefList("slide0796.htm", 1, 256),
   new hrefList("slide0797.htm", 1, 257),
   new hrefList("slide0798.htm", 1, 258),
   new hrefList("slide0799.htm", 1, 259),
   new hrefList("slide0800.htm", 1, 260),
   new hrefList("slide0801.htm", 1, 261),
   new hrefList("slide0802.htm", 1, 262),
   new hrefList("slide0803.htm", 1, 263),
   new hrefList("slide0804.htm", 1, 264),
   new hrefList("slide0805.htm", 1, 265),
   new hrefList("slide0806.htm", 1, 266),
   new hrefList("slide0807.htm", 1, 267),
   new hrefList("slide0808.htm", 1, 268),
   new hrefList("slide0809.htm", 1, 269),
   new hrefList("slide0810.htm", 1, 270)
);

function ImgBtn( oId,bId,w,action )
{
	var t=this
	t.Perform    = _IBP
	t.SetActive  = _IBSetA
 t.SetInactive= _IBSetI
	t.SetPressed = _IBSetP
	t.SetDisabled= _IBSetD
	t.Enabled    = _IBSetE
	t.ChangeIcon = null
	t.UserAction = action
	t.ChgState   = _IBUI
	t.mObjId   = oId
	t.mBorderId= bId
	t.mWidth   = w
	t.mIsOn    = t.mCurState = 0
}
function _IBSetA()
{
	if( this.mIsOn ) {
		obj=this.ChgState( gHiliteClr,gShadowClr,2 )
		obj.style.posTop=0
	}
}
function _IBSetI()
{
	if( this.mIsOn ) {
		obj=this.ChgState( gFaceClr,gFaceClr,1 )
		obj.style.posTop=0 
	}
}
function _IBSetP()
{
	if( this.mIsOn ) {
		obj=this.ChgState( gShadowClr,gHiliteClr,2 )
		obj.style.posLeft+=1; obj.style.posTop+=1
	}
}
function _IBSetD()
{  
	obj=this.ChgState( gFaceClr,gFaceClr,0 )
	obj.style.posTop=0 
}
function _IBSetE( state )
{
	var t=this
	GetObj( t.mBorderId ).style.visibility="visible"
	if( state != t.mIsOn ) {
		t.mIsOn=state
		if( state )
			t.SetInactive()
		else
			t.SetDisabled()
	}
}
function _IBP()
{
	var t=this
	if( t.mIsOn ) {
		if( t.UserAction != null )
			t.UserAction()
		if( t.ChangeIcon ) {
			obj=GetObj(t.mObjId)
			if( t.ChangeIcon() )
				obj.style.posLeft=obj.style.posLeft+(t.mCurState-4)*t.mWidth
			else
				obj.style.posLeft=obj.style.posLeft+(t.mCurState-0)*t.mWidth
		}
		t.SetActive()
	}  
}
function _IBUI( clr1,clr2,nextState )
{
	var t=this
	SetBorder( GetObj( t.mBorderId ),clr1,clr2 )
	obj=GetObj( t.mObjId )
	obj.style.posLeft=obj.style.posLeft+(t.mCurState-nextState)*t.mWidth-obj.style.posTop
	t.mCurState=nextState
	return obj
}
function TxtBtn( oId,oeId,action,chkState )
{
	var t=this
	t.Perform    = _TBP
	t.SetActive  = _TBSetA
	t.SetInactive= _TBSetI
	t.SetPressed = _TBSetP
	t.SetDisabled= _TBSetD
	t.SetEnabled = _TBSetE
	t.GetState   = chkState
	t.UserAction = action
	t.ChgState   = _TBUI
	t.mObjId      = oId
	t.m_elementsId= oeId
	t.mIsOn       = 1
}
function _TBSetA()
{
	var t=this
	if( t.mIsOn && !t.GetState() )
		t.ChgState( gHiliteClr,gShadowClr,0,0 )
}
function _TBSetI()
{
	var t=this
	if( t.mIsOn && !t.GetState() )
		t.ChgState( gFaceClr,gFaceClr,0,0 )
}
function _TBSetP()
{
	if( this.mIsOn )
		this.ChgState( gShadowClr,gHiliteClr,1,1 )
}
function _TBSetD()
{   
	this.ChgState( gFaceClr,gFaceClr,0,0 )
	this.mIsOn = 0
}
function _TBSetE()
{
	var t=this
	if( !t.GetState() )
		t.ChgState( gFaceClr,gFaceClr,0,0 )
	else
		t.ChgState( gShadowClr,gHiliteClr,1,1 )
	t.mIsOn = 1
}
function _TBP()
{
	var t=this
	if( t.mIsOn ) { 
		if( t.UserAction != null )
			t.UserAction()
		if( t.GetState() )
			t.SetPressed()
		else
			t.SetActive()
	}  
}
function _TBUI( clr1,clr2,lOffset,tOffset )
{
	SetBorder( GetObj( this.mObjId ),clr1,clr2 )
	Offset( GetObj( this.m_elementsId ),lOffset,tOffset )
}
function GetObj( objId ){ return document.all.item( objId ) }
function Offset( obj, top, left ){ obj.style.top=top; obj.style.left=left }
function SetBorder( obj, upperLeft, lowerRight )
{
	s=obj.style;
	s.borderStyle      = "solid"
	s.borderWidth      = 1 
	s.borderLeftColor  = s.borderTopColor = upperLeft
	s.borderBottomColor= s.borderRightColor = lowerRight
}
function GetBtnObj(){ return gBtnArr[window.event.srcElement.id] }
function BtnOnOver(){ b=GetBtnObj(); if( b != null ) b.SetActive() }
function BtnOnDown(){ b=GetBtnObj(); if( b != null ) b.SetPressed() }
function BtnOnOut(){ b=GetBtnObj(); if( b != null ) b.SetInactive() }
function BtnOnUp()
{
	b=GetBtnObj()
	if( b != null )
		b.Perform()
	else
		Upd()
}
function GetNtsState(){ return parent.gNtsOpen }
function GetOtlState(){ return parent.gOtlOpen }
function GetOtlTxtState(){ return parent.gOtlTxtExp }
function NtsBtnSetFlag( fVal )
{
	s=document.all.item( this.m_flagId ).style
	s.display="none"
	if( fVal )
		s.display=""
	else
		s.display="none"
}

var gHiliteClr="THREEDHIGHLIGHT",gShadowClr="THREEDSHADOW",gFaceClr="THREEDFACE"
var gBtnArr = new Array()
gBtnArr["nb_otl"] = new TxtBtn( "nb_otl","nb_otlElem",parent.ToggleOtlPane,GetOtlState )
gBtnArr["nb_nts"] = new TxtBtn( "nb_nts","nb_ntsElem",parent.ToggleNtsPane,GetNtsState )
gBtnArr["nb_prev"]= new ImgBtn( "nb_prev","nb_prevBorder",30,parent.GoToPrevSld )
gBtnArr["nb_next"]= new ImgBtn( "nb_next","nb_nextBorder",30,parent.GoToNextSld )
gBtnArr["nb_sldshw"]= new ImgBtn( "nb_sldshw","nb_sldshwBorder",18,parent.FullScreen )
gBtnArr["nb_voice"]  = new ImgBtn( "nb_voice","nb_voiceBorder",18,parent.ToggleVNarration )
gBtnArr["nb_otlTxt"]= new ImgBtn( "nb_otlTxt","nb_otlTxtBorder",23,parent.ToggleOtlText )
gBtnArr["nb_nts"].m_flagId= "notes_flag"
gBtnArr["nb_nts"].SetFlag = NtsBtnSetFlag
gBtnArr["nb_otlTxt"].ChangeIcon= GetOtlTxtState
var sNext="Next",sPrev="Previous",sEnd="End Show",sFont="Arial", alwaysOn = false
function ShowMenu()
{
	BuildMenu();
	var doc=PPTSld.document.body,x=PPTSld.event.clientX+doc.scrollLeft,y=PPTSld.event.clientY+doc.scrollTop

	m = PPTSld.document.all.item("ctxtmenu")
	m.style.pixelLeft=x
	if( (x+m.scrollWidth > doc.clientWidth)&&(x-m.scrollWidth > 0) )
		m.style.pixelLeft=x-m.scrollWidth

	m.style.pixelTop=y
	if( (y+m.scrollHeight > doc.clientHeight)&&(y-m.scrollHeight > 0) )
		m.style.pixelTop=y-m.scrollHeight

	m.style.display=""
}
function _CM()
{
	if( !parent.IsFullScrMode() && !alwaysOn) return;
	
	if(!PPTSld.event.ctrlKey) {
		ShowMenu()
		return false
	} else
		HideMenu()
}

function processNavKPH(event) {
   if ( PPTSld &&  (event.keyCode != 13 || !event.srcElement.href || event.srcElement.href == "" ) )
	return PPTSld._KPH(event);
}
function processNavClick() {
	HideMenu();
	return true;
}
function BuildMenu()
{
	if( PPTSld.document.all.item("ctxtmenu") ) return

	var mObj=CreateItem( PPTSld.document.body )
mObj.id="ctxtmenu"
	var s=mObj.style
	s.position="absolute"
 s.cursor="default"
	s.width="100px"
	SetCMBorder(mObj,"menu","black")

	var iObj=CreateItem( mObj )
	SetCMBorder( iObj, "threedhighlight","threedshadow" )
	iObj.style.padding=2
	if ( self.IsFullScrMode() ) {
		CreateMenuItem( iObj,sNext,M_GoNextSld,M_True )
		CreateMenuItem( iObj,sPrev,M_GoPrevSld,M_HasPrevSld )
	}
	else {
		CreateMenuItem( iObj,sNext, base.TP_GoToNextSld, base.HasNextSld )
		CreateMenuItem( iObj,sPrev,base.GoToPrevSld, base.HasPrevSld )
	}
	var sObj=CreateItem( iObj )
	SetCMBorder(sObj,"menu","menu")
	var s=sObj.style
	s.borderTopColor="threedshadow"
	s.borderBottomColor="threedhighlight"
	s.height=1
	s.fontSize="0px"
	if ( self.IsFullScrMode() ) 
		CreateMenuItem( iObj,sEnd,M_End,M_True )
	else
		CreateMenuItem( iObj,sEnd,M_End,M_False )
}
function Highlight() { ChangeClr("activecaption","threedhighlight") }
function Deselect() { ChangeClr("threedface","menutext") }
function Perform()
{
	e=PPTSld.event.srcElement
	if( e.type=="menuitem" && e.IsActive() )
		e.Action()
	else
		PPTSld.event.cancelBubble=true
}
function ChangeClr( bg,clr )
{
	e=PPTSld.event.srcElement
	if( e.type=="menuitem" && e.IsActive() ) {
		e.style.backgroundColor=bg
		e.style.color=clr
	}
}

function M_HasPrevSld() { return( base.HasPrevSld() ) }
function M_GoNextSld() { 
	base.SetFSMode(1);
	if( gIsEndShow )
		 M_End();
	else {
		if ( base.HasNextSld() )
		 base.GoToNextSld();
		else if (  base.EndSlideShow ) {
		 StartEndShow();
		 gIsEndShow = 1;
		 
		 PPTNav.location.reload();
		}
		else
			base.CloseFullScreen();
	}
}
function M_GoPrevSld() {
	base.SetFSMode(1);
	g_hideNav = 0;
	if( gIsEndShow ) { 
		gIsEndShow = 0;
		if ( base.msie > 0 && IsMac() ) 
			ChangeFrame( SLIDE_FRAME, GetHrefObj( g_currentSlide ).m_slideHref );
		else	
		PPTSld.history.back();
		
		 PPTNav.location.reload();
		if( PPTSld.event )
			 PPTSld.event.cancelBubble=true;
	}
	else
	 	base.GoToPrevSld();
}
function M_True() { return true }
function M_False() { return false }

function M_End() {
	base.CloseFullScreen();
	/*PPTSld.event.cancelBubble=true;
	window.close( self )*/
}

function CreateMenuItem( node,text,action,eval )
{
	var e=CreateItem( node )
	e.type="menuitem"
	e.Action=action
	e.IsActive=eval
	e.innerHTML=text

	if( !e.IsActive() )
		e.style.color="threedshadow"
	e.onclick=Perform
	e.onmouseover=Highlight
	e.onmouseout=Deselect
	s=e.style;
	s.fontFamily=sFont
	s.fontSize="8pt"
	s.paddingLeft=2
}
function CreateItem( node )
{
	var elem=PPTSld.document.createElement("DIV")
	node.insertBefore( elem )
	return elem
}
function SetCMBorder( o,ltClr,rbClr )
{
	var s=o.style
	s.backgroundColor="menu"
	s.borderStyle="solid"
	s.borderWidth=1
	s.borderColor=ltClr+" "+rbClr+" "+rbClr+" "+ltClr
}

/* netscape context menu */
g_ctxmenu = 0;
function setRect( obj, X, Y, W, H ) {
	obj.top = Y;
	obj.left = X;
	obj.clip.top = 0;
	obj.clip.left = 0;
	obj.clip.bottom = H;
	obj.clip.right = W;
}	

function KPH(event) {
	if ( ! base.IsFullScrMode() && !alwaysOn )
		return true;
		
	if ( (!IsMac() &&event.which == 3) || ( IsMac() && (event.modifiers & Event.CONTROL_MASK) && event.which == 1 )   ) {
		PPTSld.g_ctxmenu = 1;
		PPTSld.stripUobj.visibility = "show";
		PPTSld.stripDobj.visibility = "show";
		PPTSld.shadeUobj.visibility = "show";
		PPTSld.shadeDobj.visibility = "show";
		PPTSld.panelobj.visibility = "show";
		PPTSld.Fobj.visibility = "show";
		PPTSld.Bobj.visibility = "show";
		PPTSld.Eobj.visibility = "show";

		setRect(PPTSld.shadeUobj, event.pageX-2, event.pageY-2, 82, 67 );		
		setRect(PPTSld.shadeDobj, event.pageX, event.pageY, 82, 67 );		
		setRect(PPTSld.panelobj, event.pageX, event.pageY, 80, 65 );		
		setRect(PPTSld.Fobj, event.pageX, event.pageY, 80, 20 );
		setRect(PPTSld.Bobj, event.pageX, event.pageY+20, 80, 20 );
		setRect(PPTSld.stripUobj, event.pageX, event.pageY+41, 80, 1 );		
		setRect(PPTSld.stripDobj, event.pageX, event.pageY+43, 80, 1 );		
		setRect(PPTSld.Eobj, event.pageX, event.pageY+45, 80, 20 );
		return false;
	}
	if ( HitOK( event ) ) {
	PPTSld.g_ctxmenu = 0;
		PPTSld.stripUobj.visibility = "hide";
		PPTSld.stripDobj.visibility = "hide";
		PPTSld.shadeUobj.visibility = "hide";
		PPTSld.shadeDobj.visibility = "hide";
		PPTSld.panelobj.visibility = "hide";
		PPTSld.Fobj.visibility = "hide";
		PPTSld.Bobj.visibility = "hide";
		PPTSld.Eobj.visibility = "hide";
	}
	return true;
}

function overMe() {
	this.bgColor = "blue";
}

function outMe() {
	this.bgColor = "#AAAAAA"; 
}

function makeElement( whichEl, whichContainer ) {
	if ( arguments.length == 1 ) {
		whichContainer = PPTSld;
	}
	tmp = new Layer(100,whichContainer);
	eval( whichEl + " = tmp" );
	return eval(whichEl);
}

function initMe( obj, clr, text ) {
	obj.bgColor = clr;
//	obj.document.write("<a href='javascript:return false'>" + text + "</a>");
	obj.document.write( "<font size=2 face=Arial " );
	if ( !M_HasPrevSld() && (obj == PPTSld.Bobj )  ) {
		obj.document.write( " color='#808080' " );
	}
	else {
		obj.onmouseover = overMe;
		obj.onmouseout = outMe;
	}	
	obj.document.write( " > &nbsp " + text +"</font> <layer top=0 left=0 width=100 height=40 ></layer>");
	obj.document.close();
	obj.captureEvents(Event.CLICK);
	obj.color = "black";		
}

function createCM() {
  if ( base.IsFullScrMode() ) {
  	var clr = "#AAAAAA";
	PPTSld.shadeUobj = makeElement("SHADEU");
	PPTSld.shadeDobj = makeElement("SHADED");
	PPTSld.panelobj = makeElement("PANEL");
	PPTSld.stripUobj = makeElement("STRIPU");
	PPTSld.stripDobj = makeElement("STRIPD");
	PPTSld.shadeUobj.bgColor = "#BBBBBB";
	PPTSld.shadeDobj.bgColor = "#888888";
	PPTSld.stripUobj.bgColor = "#777777";
	PPTSld.stripDobj.bgColor = "#CCCCCC";
	PPTSld.panelobj.bgColor = clr;
	PPTSld.Fobj = makeElement("Next");
	PPTSld.Bobj = makeElement("Previous");
	PPTSld.Eobj = makeElement("EndShow");
	initMe( PPTSld.Fobj, clr, "Next" );
	PPTSld.Fobj.onclick = M_GoNextSld;

	initMe( PPTSld.Bobj, clr, "Previous" );
	PPTSld.Bobj.onclick = M_GoPrevSld;

	initMe( PPTSld.Eobj, clr, "End Show");
	PPTSld.Eobj.onclick = base.CloseFullScreen;
  }
}

function IsContextMenu() {
	return (g_ctxmenu == 1)
}
var g_notesTable = new Array()
var g_hiddenSlide = new Array()
makeSlide( 0,0,1);
makeSlide( 1,0,1);
makeSlide( 2,0,1);
makeSlide( 3,0,1);
makeSlide( 4,0,1);
makeSlide( 5,0,1);
makeSlide( 6,0,1);
makeSlide( 7,0,1);
makeSlide( 8,0,1);
makeSlide( 9,0,1);
makeSlide( 10,0,1);
makeSlide( 11,0,1);
makeSlide( 12,0,1);
makeSlide( 13,0,1);
makeSlide( 14,0,1);
makeSlide( 15,0,1);
makeSlide( 16,0,1);
makeSlide( 17,0,1);
makeSlide( 18,0,1);
makeSlide( 19,0,1);
makeSlide( 20,0,1);
makeSlide( 21,0,1);
makeSlide( 22,0,1);
makeSlide( 23,0,1);
makeSlide( 24,0,1);
makeSlide( 25,0,1);
makeSlide( 26,0,1);
makeSlide( 27,0,1);
makeSlide( 28,0,1);
makeSlide( 29,0,1);
makeSlide( 30,0,1);
makeSlide( 31,0,1);
makeSlide( 32,0,1);
makeSlide( 33,0,1);
makeSlide( 34,0,1);
makeSlide( 35,0,1);
makeSlide( 36,0,1);
makeSlide( 37,0,1);
makeSlide( 38,0,1);
makeSlide( 39,0,1);
makeSlide( 40,0,1);
makeSlide( 41,0,1);
makeSlide( 42,0,1);
makeSlide( 43,0,1);
makeSlide( 44,0,1);
makeSlide( 45,0,1);
makeSlide( 46,0,1);
makeSlide( 47,0,1);
makeSlide( 48,0,1);
makeSlide( 49,0,1);
makeSlide( 50,0,1);
makeSlide( 51,0,1);
makeSlide( 52,0,1);
makeSlide( 53,0,1);
makeSlide( 54,0,1);
makeSlide( 55,0,1);
makeSlide( 56,0,1);
makeSlide( 57,0,1);
makeSlide( 58,0,1);
makeSlide( 59,0,1);
makeSlide( 60,0,1);
makeSlide( 61,0,1);
makeSlide( 62,0,1);
makeSlide( 63,0,1);
makeSlide( 64,0,1);
makeSlide( 65,0,1);
makeSlide( 66,0,1);
makeSlide( 67,0,1);
makeSlide( 68,0,1);
makeSlide( 69,0,1);
makeSlide( 70,0,1);
makeSlide( 71,0,1);
makeSlide( 72,0,1);
makeSlide( 73,0,1);
makeSlide( 74,0,1);
makeSlide( 75,0,1);
makeSlide( 76,0,1);
makeSlide( 77,0,1);
makeSlide( 78,0,1);
makeSlide( 79,0,1);
makeSlide( 80,0,1);
makeSlide( 81,0,1);
makeSlide( 82,0,1);
makeSlide( 83,0,1);
makeSlide( 84,0,1);
makeSlide( 85,0,1);
makeSlide( 86,0,1);
makeSlide( 87,0,1);
makeSlide( 88,0,1);
makeSlide( 89,0,1);
makeSlide( 90,0,1);
makeSlide( 91,0,1);
makeSlide( 92,0,1);
makeSlide( 93,0,1);
makeSlide( 94,0,1);
makeSlide( 95,0,1);
makeSlide( 96,0,1);
makeSlide( 97,0,1);
makeSlide( 98,0,1);
makeSlide( 99,0,1);
makeSlide( 100,0,1);
makeSlide( 101,0,1);
makeSlide( 102,0,1);
makeSlide( 103,0,1);
makeSlide( 104,0,1);
makeSlide( 105,0,1);
makeSlide( 106,0,1);
makeSlide( 107,0,1);
makeSlide( 108,0,1);
makeSlide( 109,0,1);
makeSlide( 110,0,1);
makeSlide( 111,0,1);
makeSlide( 112,0,1);
makeSlide( 113,0,1);
makeSlide( 114,0,1);
makeSlide( 115,0,1);
makeSlide( 116,0,1);
makeSlide( 117,0,1);
makeSlide( 118,0,1);
makeSlide( 119,0,1);
makeSlide( 120,0,1);
makeSlide( 121,0,1);
makeSlide( 122,0,1);
makeSlide( 123,0,1);
makeSlide( 124,0,1);
makeSlide( 125,0,1);
makeSlide( 126,0,1);
makeSlide( 127,0,1);
makeSlide( 128,0,1);
makeSlide( 129,0,1);
makeSlide( 130,0,1);
makeSlide( 131,0,1);
makeSlide( 132,0,1);
makeSlide( 133,0,1);
makeSlide( 134,0,1);
makeSlide( 135,0,1);
makeSlide( 136,0,1);
makeSlide( 137,0,1);
makeSlide( 138,0,1);
makeSlide( 139,0,1);
makeSlide( 140,0,1);
makeSlide( 141,0,1);
makeSlide( 142,0,1);
makeSlide( 143,0,1);
makeSlide( 144,0,1);
makeSlide( 145,0,1);
makeSlide( 146,0,1);
makeSlide( 147,0,1);
makeSlide( 148,0,1);
makeSlide( 149,0,1);
makeSlide( 150,0,1);
makeSlide( 151,0,1);
makeSlide( 152,0,1);
makeSlide( 153,0,1);
makeSlide( 154,0,1);
makeSlide( 155,0,1);
makeSlide( 156,0,1);
makeSlide( 157,0,1);
makeSlide( 158,0,1);
makeSlide( 159,0,1);
makeSlide( 160,0,1);
makeSlide( 161,0,1);
makeSlide( 162,0,1);
makeSlide( 163,0,1);
makeSlide( 164,0,1);
makeSlide( 165,0,1);
makeSlide( 166,0,1);
makeSlide( 167,0,1);
makeSlide( 168,0,1);
makeSlide( 169,0,1);
makeSlide( 170,0,1);
makeSlide( 171,0,1);
makeSlide( 172,0,1);
makeSlide( 173,0,1);
makeSlide( 174,0,1);
makeSlide( 175,0,1);
makeSlide( 176,0,1);
makeSlide( 177,0,1);
makeSlide( 178,0,1);
makeSlide( 179,0,1);
makeSlide( 180,0,1);
makeSlide( 181,0,1);
makeSlide( 182,0,1);
makeSlide( 183,0,1);
makeSlide( 184,0,1);
makeSlide( 185,0,1);
makeSlide( 186,0,1);
makeSlide( 187,0,1);
makeSlide( 188,0,1);
makeSlide( 189,0,1);
makeSlide( 190,0,1);
makeSlide( 191,0,1);
makeSlide( 192,0,1);
makeSlide( 193,0,1);
makeSlide( 194,0,1);
makeSlide( 195,0,1);
makeSlide( 196,0,1);
makeSlide( 197,0,1);
makeSlide( 198,0,1);
makeSlide( 199,0,1);
makeSlide( 200,0,1);
makeSlide( 201,0,1);
makeSlide( 202,0,1);
makeSlide( 203,0,1);
makeSlide( 204,0,1);
makeSlide( 205,0,1);
makeSlide( 206,0,1);
makeSlide( 207,0,1);
makeSlide( 208,0,1);
makeSlide( 209,0,1);
makeSlide( 210,0,1);
makeSlide( 211,0,1);
makeSlide( 212,0,1);
makeSlide( 213,0,1);
makeSlide( 214,0,1);
makeSlide( 215,0,1);
makeSlide( 216,0,1);
makeSlide( 217,0,1);
makeSlide( 218,0,1);
makeSlide( 219,0,1);
makeSlide( 220,0,1);
makeSlide( 221,0,1);
makeSlide( 222,0,1);
makeSlide( 223,0,1);
makeSlide( 224,0,1);
makeSlide( 225,0,1);
makeSlide( 226,0,1);
makeSlide( 227,0,1);
makeSlide( 228,0,1);
makeSlide( 229,0,1);
makeSlide( 230,0,1);
makeSlide( 231,0,1);
makeSlide( 232,0,1);
makeSlide( 233,0,1);
makeSlide( 234,0,1);
makeSlide( 235,0,1);
makeSlide( 236,0,1);
makeSlide( 237,0,1);
makeSlide( 238,0,1);
makeSlide( 239,0,1);
makeSlide( 240,0,1);
makeSlide( 241,0,1);
makeSlide( 242,0,1);
makeSlide( 243,0,1);
makeSlide( 244,0,1);
makeSlide( 245,0,1);
makeSlide( 246,0,1);
makeSlide( 247,0,1);
makeSlide( 248,0,1);
makeSlide( 249,0,1);
makeSlide( 250,0,1);
makeSlide( 251,0,1);
makeSlide( 252,0,1);
makeSlide( 253,0,1);
makeSlide( 254,0,1);
makeSlide( 255,0,1);
makeSlide( 256,0,1);
makeSlide( 257,0,1);
makeSlide( 258,0,1);
makeSlide( 259,0,1);
makeSlide( 260,0,1);
makeSlide( 261,0,1);
makeSlide( 262,0,1);
makeSlide( 263,0,1);
makeSlide( 264,0,1);
makeSlide( 265,0,1);
makeSlide( 266,0,1);
makeSlide( 267,0,1);
makeSlide( 268,0,1);
makeSlide( 269,0,1);

var END_SHOW_HREF         = "endshow.htm",
    OUTLINE_EXPAND_HREF   = "outline_expanded.htm",
    OUTLINE_COLLAPSE_HREF = "outline_collapsed.htm",
    OUTLINE_NAVBAR_HREF  = "outline_navigation_bar.htm",
    NAVBAR_HREF           = "navigation_bar.htm",
    BLANK_NOTES_HREF	  = "blank_notes.htm",
    NUM_VISIBLE_SLIDES    = 270,
    SIMPLE_FRAMESET       = 0,
    SLIDE_FRAME	        = "PPTSld",
    NOTES_FRAME           = "PPTNts",
    OUTLINE_FRAME         = "PPTOtl",
    OUTLINE_NAVBAR_FRAME  = "PPTOtlNav",
    NAVBAR_FRAME          = "PPTNav",
	MAIN_FRAME			  = "MainFrame",
	FS_NAVBAR_HREF		  = "fs_navigation_bar.htm",
	isIEFiles 			= 0,
	isNAVFiles 			= 0,
	isFLATFiles 			= 16,
	includeNotes			= 0,
	PPTPRESENTATION     = 1;
var  INITSLIDENUM   = 1;

var EndSlideShow = 0;
var g_outline_href = OUTLINE_COLLAPSE_HREF;	
var g_fullscrMode = 0;	
var FSWin = null;
var gtmpstr = document.location.href;
var g_baseURL = gtmpstr.substr(0, gtmpstr.lastIndexOf("/") ) + "/" + "VAAM2_files";
var g_showoutline = 1;
var g_shownotes = includeNotes;
var g_currentSlide = INITSLIDENUM, g_prevSlide = INITSLIDENUM;
var saveFSSlideNum = saveTPSlideNum = g_currentSlide;
var saveFSprevSlide = saveTPprevSlide = g_prevSlide;
var g_slideType="ie";
var appVer = navigator.appVersion;
var msie = appVer.indexOf( "MSIE " ) + appVer.indexOf( "Internet Explorer " );
var isnav = ( navigator.appName.indexOf( "Netscape" ) >= 0 );
var msieWin31 = (appVer.indexOf( "Windows 3.1" ) > 0);
var ver = 0;
var g_done = 0;
var g_prevotlobjidx = 0;
var g_ShowFSDefault = 0;
var g_lastVisibleSld = 1;
var g_allHidden = false;
function IsIE() {
	return (msie >= 0 );
}

function IsNav() {
	return (isnav);
}
var msiePos = appVer.indexOf( "MSIE " );
var inexPos = appVer.indexOf( "Internet Explorer " );
if ( msiePos >= 0 )
  ver = parseFloat( appVer.substring( msiePos+5, appVer.indexOf ( ";", msiePos ) ) );
else if( inexPos >= 0 )
  ver=parseFloat( appVer.substring( inexPos+18, appVer.indexOf(";",inexPos) ) )
else
  ver = parseInt( appVer );

//var g_supportsPPTHTML = 0; //!msieWin31 && ( ( msie >= 0 && ver >= 3.02 ) || ( msie < 0 && ver >= 3 ) );

function GetCurrentSlideNum()
{   
  obj = GetHrefObj( g_currentSlide );
  if ( GetHrefObj( g_currentSlide ).m_origVisibility == 1 )
    return obj.m_slideIdx;
  else   
    return g_currentSlide;
}

function GetNumSlides()
{
  if ( GetHrefObj( g_currentSlide ).m_origVisibility == 1 )
    return NUM_VISIBLE_SLIDES;
  else
    return g_docTable.length;
}

function GetHrefObj( slideIdx )
{ return g_docTable[slideIdx - 1];
}

function GetSlideNum( slideHref )
{
  for (ii=0; ii<g_docTable.length; ii++) {
    if ( g_docTable[ii].m_slideHref == slideHref )
      return ii+1;
  }
  return 1;
}

function GoToNextSld()
{   
  targetIdx = g_currentSlide + 1;
  if ( GetHrefObj( targetIdx-1 ).m_origVisibility == 0 ) {
    if ( targetIdx<=g_docTable.length ) {
      obj = GetHrefObj( targetIdx );
      obj.m_visibility = 1;
      GoToSld( obj.m_slideHref );
    }
  }
  else {
    obj = GetHrefObj( targetIdx );
    while ( obj && ( obj.m_origVisibility == 0 ) && ( targetIdx<=g_docTable.length ) )
      obj = GetHrefObj( targetIdx++ );
    if( obj && obj.m_origVisibility )
      GoToSld( obj.m_slideHref );
  }
}

function GoToPrevSld()
{
  targetIdx = g_currentSlide - 1;
  if ( targetIdx > 0 ) {
    obj = GetHrefObj( targetIdx );
    while ( ( obj.m_visibility == 0 ) && ( targetIdx>0 ) )
      obj = GetHrefObj( targetIdx-- );
    GoToSld( obj.m_slideHref );
  }
}

function GoToLast()
{
  targetIdx = g_docTable.length;
  if ( targetIdx != g_currentSlide )
    GoToSld( GetHrefObj( targetIdx ).m_slideHref );
}

function GoToFirst()
{ GoToSld( GetHrefObj(1).m_slideHref );
}

function highlite() {
	if ( IsFullScrMode() )
		return;
	index = GetCurrentSlideNum();
	if ( !frames[MAIN_FRAME].frames[OUTLINE_FRAME] )
		return;
	if ( msie < 0 ) {
		if ( g_prevotlobjidx != 0 ) {
			eval( "otlobj = frames[MAIN_FRAME].frames[OUTLINE_FRAME].document.LAYERID" + g_prevotlobjidx );
			otlobj.hidden = true;
		}
		else
			index = GetCurrentSlideNum();
		eval( "otlobj = frames[MAIN_FRAME].frames[OUTLINE_FRAME].document.LAYERID" + index );
		otlobj.hidden = false;
	
		g_prevotlobjidx = index;
		
		return;
	}
	if ( !g_showoutline )
		return;
		
		backclr = frames[MAIN_FRAME].frames[OUTLINE_FRAME].document.body.bgColor;
		textclr = frames[MAIN_FRAME].frames[OUTLINE_FRAME].document.body.text;
	if ( g_prevotlobjidx != 0 ) {
		eval( "otlobj = frames[MAIN_FRAME].frames[OUTLINE_FRAME].document.all.p" + g_prevotlobjidx );
		otlobj.style.backgroundColor = backclr;
		otlobj.style.color = textclr;
		otlobj.all.AREF.style.color = textclr;
	}
	else
		index = GetCurrentSlideNum();
	eval( "otlobj = frames[MAIN_FRAME].frames[OUTLINE_FRAME].document.all.p" + index );
	otlobj.style.backgroundColor = textclr;
	otlobj.style.color = backclr;
	otlobj.all.AREF.style.color = backclr;
	g_prevotlobjidx = index;
}

function ChangeFrame( frame, href )
{
if ( IsFramesMode() ) {
  if ( NAVBAR_FRAME == frame || OUTLINE_NAVBAR_FRAME ==  frame ) {
	    frames[frame].location.replace(href);
  }
  else if( ! ( ( OUTLINE_FRAME == frame && !g_showoutline)  || (NOTES_FRAME == frame && !g_shownotes ) ) ){
	    frames[MAIN_FRAME].frames[frame].location.href = href;
  }
 }
 else {
 	if ( frame == NAVBAR_FRAME || frame == SLIDE_FRAME ) {
 	  if( frame == NAVBAR_FRAME ) {
 	  	 href = FS_NAVBAR_HREF;
 	  	
 	  }	    
 	  if( frame == NAVBAR_FRAME ) 
	      window.frames[frame].location.replace(href);
	 else
	      window.frames[frame].location.href = href;
 	}
 }
  
}

function shutEventPropagation() {
	if ( IsNav() )
		return;
		
	var slideFrame;
	if ( IsFramesMode() )
		slideFrame = frames[MAIN_FRAME].frames[SLIDE_FRAME];
	else
		slideFrame = window.frames[SLIDE_FRAME];
	if ( slideFrame.event ) 
		slideFrame.event.cancelBubble=true;
}
				
function GoToSld( slideHref )
{
  shutEventPropagation();
  if ( slideHref != GetHrefObj( g_currentSlide ).m_slideHref || g_slideType != GetHrefObj( g_currentSlide ).type) {
    g_prevSlide = g_currentSlide;
    g_currentSlide = GetSlideNum( slideHref );
	g_slideType = GetHrefObj( g_currentSlide ).type;
    obj = GetHrefObj( g_currentSlide );
    obj.m_visibility = 1;
    ChangeFrame( SLIDE_FRAME, slideHref );
    if( !SIMPLE_FRAMESET )
      ChangeFrame( NOTES_FRAME, obj.m_notesHref );
    ChangeFrame( NAVBAR_FRAME, NAVBAR_HREF );
	    
  }
}

function PrevSldViewed()
{ GoToSld( GetHrefObj( g_prevSlide ).m_slideHref );
}

function NoHref() {}

function ExpandOutline( )
{ 
 g_outline_href = OUTLINE_EXPAND_HREF;
 ChangeFrame( OUTLINE_FRAME, OUTLINE_EXPAND_HREF );
 frames[OUTLINE_NAVBAR_FRAME].location.replace( OUTLINE_NAVBAR_HREF);
}

function CollapseOutline()
{ 
 g_outline_href = OUTLINE_COLLAPSE_HREF;
 ChangeFrame( OUTLINE_FRAME, OUTLINE_COLLAPSE_HREF );
 frames[OUTLINE_NAVBAR_FRAME].location.replace( OUTLINE_NAVBAR_HREF);
 }

function SlideUpdated( id )
{
  if ( id != GetHrefObj( g_currentSlide ).m_slideHref )  {
    g_prevSlide = g_currentSlide;
    g_currentSlide = GetSlideNum( id );
    obj = GetHrefObj( g_currentSlide );
    if( !SIMPLE_FRAMESET )
      ChangeFrame( NOTES_FRAME, obj.m_notesHref );
    ChangeFrame( NAVBAR_FRAME, NAVBAR_HREF );
  }
}

function hrefList( slideHref, notesHref, visible, slideIdx, type )
{
  this.m_slideHref  = slideHref;
  this.m_notesHref  = notesHref;
  this.m_navbarHref = NAVBAR_HREF;
  this.m_origVisibility = visible;
  this.m_visibility = visible;
  this.m_slideIdx = slideIdx;
  this.type = type;
}

function IsFullScrMode() {
	return g_fullscrMode;
}


function IsFramesMode() {
	return (1 - g_fullscrMode);
}

function SldUpdated( id )
{
  if ( ( id != GetHrefObj( g_currentSlide ).m_slideHref )  || ( g_currentSlide == g_lastVisibleSld ) ){
    g_prevSlide = g_currentSlide;
    g_currentSlide = GetSlideNum( id );
    obj = GetHrefObj( g_currentSlide );
    if( !SIMPLE_FRAMESET )
      ChangeFrame( NOTES_FRAME, obj.m_notesHref );
    ChangeFrame( NAVBAR_FRAME, NAVBAR_HREF );
  }
}

function ToggleOutline() {
	g_showoutline = 1 - g_showoutline;
	writeMyFrame();
}

function ShowHideNotes() {
	g_shownotes = 1 - g_shownotes;
	writeMyFrame();
}

function writeMyFrame() {
		SetFSMode(0);
		obj = frames[MAIN_FRAME];
		
		var curslide = g_baseURL + "/" +  GetHrefObj( g_currentSlide ).m_slideHref;
		var curnotes = g_baseURL + "/" +  GetHrefObj( g_currentSlide ).m_notesHref;
		var otlhref = g_baseURL + "/" +  g_outline_href;
		if ( msie < 0 ) {			
		if ( ! g_showoutline && g_shownotes ) {
			obj.document.write( '<HTML><HEAD><SCRIPT language=JavaScript src=' + g_baseURL + '/script.js></SCRIPT><SCRIPT> base = parent; <\/SCRIPT><\/HEAD> \
				<frameset rows=\"*,20%\" id=\"frameset2\" > \
				<frame src=\"' + curslide + '\" name=PPTSld marginheight=0 marginwidth=0> \
				<frame src=\"' + curnotes + '\" name=PPTNts marginheight=0 marginwidth=0> \
				</frameset> </html>' );
		}
		else if( g_showoutline && g_shownotes  ){
			obj.document.write( '<HTML><HEAD><SCRIPT language=JavaScript src=' + g_baseURL + '/script.js></SCRIPT><SCRIPT> base = parent; <\/SCRIPT><\/HEAD> \
				<frameset cols=\"20%,*\" id=\"frameset1\"> \
				<frame src=\"' + otlhref + '\" name=PPTOtl> \
				<frameset rows=\"*,20%\" id=\"frameset2\" > \
				<frame src=\"' + curslide + '\" name=PPTSld marginheight=0 marginwidth=0> \
				<frame src=\"' + curnotes + '\" name=PPTNts marginheight=0 marginwidth=0> \
				</frameset> </frameset></html>' );
		}		
		else if ( !g_shownotes && !g_showoutline ) {
			obj.document.write( '<HTML><HEAD><SCRIPT language=JavaScript src=' + g_baseURL + '/script.js></SCRIPT><SCRIPT> base = parent; <\/SCRIPT><\/HEAD> \
				<frameset rows="*,0" frameborder=0 > \
				<frame src=\"' + curslide + '\" name=PPTSld marginheight=0 marginwidth=0> \
				</frameset> </html>' );
		}
		else if( !g_shownotes  && g_showoutline ) {
			obj.document.write( '<HTML><HEAD><SCRIPT language=JavaScript src=' + g_baseURL + '/script.js></SCRIPT><SCRIPT> base = parent; <\/SCRIPT><\/HEAD> \
				<frameset cols=\"20%,*\" id=\"frameset1\"> \
				<frame src=\"' + otlhref + '\" name=PPTOtl> \
				<frame src=\"' + curslide + '\" name=PPTSld marginheight=0 marginwidth=0> \
				</frameset></html>' );
		}
		obj.document.close();
		}
		else {
			if ( g_showoutline ) {
				obj.PPTHorizAdjust.cols = "20%,*";
				obj.PPTOtl.location.reload();
			}
			else {
				obj.PPTHorizAdjust.cols = "0,*";
			}
			if ( g_shownotes ) {
				obj.PPTVertAdjust.rows = "*,20%";
				obj.PPTNts.location.href = curnotes;
			}
			else {
				obj.PPTVertAdjust.rows = "*,0";
			}
		}
		ChangeFrame( OUTLINE_NAVBAR_FRAME, OUTLINE_NAVBAR_HREF );
}

function FullScreen() {
	g_done = 0;

	
	SetFSMode(1);
	if ( msie >= 0 )
		FSWin = window.open( g_baseURL + "/" + "fullscreen.htm", null, "fullscreen=yes");
	else {
		var height = screen.availHeight;
		if ( window.navigator.platform.indexOf( "Mac" ) >= 0 ) {
			height -= 30;
		}
		FSWin = window.open( g_baseURL + "/" + "fullscreen.htm", "null", "height="+ height + ",width=" + screen.availWidth + ",screenX=0,screenY=0");
	}
}

function SetFSMode( i ) {

}

function Slide( i ) {
	SetFSMode(0);
	GoToSld(GetHrefObj(i).m_slideHref);
}

function TP_GoToNextSld() {
	SetFSMode(0);
	GoToNextSld();
}

function TP_GoToPrevSld() {
	SetFSMode(0);
	GoToPrevSld();
}

function CloseFullScreen() {
	g_done = 0;	
	
	if ( IsNav() ){
		if ( self.opener )
			opener.FSWin = null;
	}
	window.close();
}

function slidenum(i) {
	var slidename = "slide";
	if ( i < 10 )
		return ( slidename + "000" + i);
	else if ( i < 100 )
		return ( slidename + "00" + i );
	else if ( i < 1000 ) 
		return (slidename + "0" + i );
	else
		return (slidename + i );
}
function UpdateLastVisibleSlide( index ) {
	if ( g_lastVisibleSld < index ) 
		g_lastVisibleSld = index;
}

function jpegArray( numSlides ) {
count_hidden = 0;
	g_docTable = new Array();
  for( i=0; i<numSlides; i++ ) {
    j = 2 * numSlides + i + 1;
    var str = slidenum( j ) +".htm";
	if( g_notesTable[i] == 1 )
		g_docTable[i] = new hrefList( str, slidenum(i+1 ) + "_notes_pane.htm", g_hiddenSlide[i], i+1-count_hidden, "jpeg" );
	else
		g_docTable[i] = new hrefList( str, BLANK_NOTES_HREF, g_hiddenSlide[i], i+1-count_hidden, "jpeg" );
    if ( !g_hiddenSlide[i] ) count_hidden++;
    else UpdateLastVisibleSlide( i+1 );
  }
}

function ieArray( numSlides ) {
count_hidden = 0;
	g_docTable = new Array();
  for( i=0; i<numSlides; i++ ) {
    var str = slidenum(i+1) +".htm";
	if( g_notesTable[i] == 1 )
		g_docTable[i] = new hrefList( str, slidenum( i+1 ) + "_notes_pane.htm", g_hiddenSlide[i], i+1-count_hidden, "ie" );
	else
		g_docTable[i] = new hrefList( str, BLANK_NOTES_HREF, g_hiddenSlide[i], i+1-count_hidden, "ie" );
    if ( !g_hiddenSlide[i] ) count_hidden++;
    else UpdateLastVisibleSlide( i+1 );
  }
}

function navArray( numSlides ) {
count_hidden = 0;
	g_docTable = new Array();
  for( i=0; i<numSlides; i++ ) {
    j = numSlides + i + 1;
    var str = slidenum( j ) +".htm";
	if( g_notesTable[i] == 1 )
		g_docTable[i] = new hrefList( str, slidenum(i+1 ) + "_notes_pane.htm", g_hiddenSlide[i], i+1-count_hidden, "nav" );
	else
		g_docTable[i] = new hrefList( str, BLANK_NOTES_HREF, g_hiddenSlide[i], i+1-count_hidden, "nav" );
    if ( !g_hiddenSlide[i] ) count_hidden++;
    else UpdateLastVisibleSlide( i+1 );
  }
}

function LoadHTMLVersion() {
  var os = window.navigator.platform.indexOf("Mac");
  if ( (msie || isnav ) && ( (os < 0 && ver >= 4 ) || ( os >= 0 && ver >= 5 ) || (os >=0 && msie < 0 && ver >= 4 ) )  ){
	if ( msie >= 0 )  {
		if ( isIEFiles > 0 )
			ieArray( 270 );
		else if ( isFLATFiles > 0 ){
			/*if ( IsFramesMode() )
				StatusPlay("This presentation is optimized for use with older versions of your browser. Since you are using a more recent version of Microsoft Internet Explorer or Netscape Navigator, consider optimizing this presentation to take advantage of your current version's advanced capabilities."); */
			jpegArray( 270 );
		}
		else
			window.location.replace(  "VAAM2_files/error.htm" );
	}
	else {
		if ( isNAVFiles > 0 && ver < 5) 
			navArray( 270 );
		else if ( isFLATFiles > 0 ) {
			/* if ( IsFramesMode() )
				StatusPlay("This presentation is optimized for use with older versions of your browser. Since you are using a more recent version of Microsoft Internet Explorer or Netscape Navigator, consider optimizing this presentation to take advantage of your current version's advanced capabilities."); */
			jpegArray( 270 );
		}
		else
			window.location.replace(  "VAAM2_files/error.htm" );
	}
}
else {
	/*
	if ( IsFramesMode() && !isWebTV() )
		StatusPlay("This presentation contains content that your browser may not be able to show properly. This presentation was optimized for more recent versions of Microsoft Internet Explorer or Netscape Navigator.");
	*/
	if ( isFLATFiles <= 0 ) {
	/*	if ( IsFramesMode() )
			window.alert("This presentation contains content that your browser may not be able to display properly. This presentation is optimized for more recent versions of Microsoft Internet Explorer or Netscape Navigator." );
	*/
		window.location.replace(  "VAAM2_files/error.htm" );
	}		
	/*
	else if ( IsFramesMode()  && !isWebTV() )
		StatusPlay( "This presentation contains content that your browser may not be able to show properly. This presentation was optimized for more recent versions of Microsoft Internet Explorer or Netscape Navigator." ); 
	*/	
	jpegArray ( 270 );
  }
  
}

function isWebTV() {
	if ( window.navigator.appName.indexOf( 'WebTV' ) >= 0 )
		return true;
	return false;
}
		
var count;
var statusText;
var statusfirst = 0;
 function display50( text ) 
{
	len = text.length;
	if ( len < 50 && count < 2) {
		window.status = text;
		window.setTimeout( "repeat()", 300 );
	}	
	else {
		var period = 200;
		window.status = text;
		newtext = text.substring( 1, len );
		if ( statusfirst ) {
			statusfirst = 0;
			period = 2000;
		}	
		window.setTimeout( "display50( newtext )", period );
	}
}
function repeat(  ) {
	count++;		
	statusfirst = 1;
	display50( statusText );
}

function StatusPlay( text ) {
	count = 0;
	statusText = text;
	repeat( );		
 }
function makeSlide( i, notes, visible ) {
	g_notesTable[i] = notes;
	g_hiddenSlide[i] = visible;
}	

