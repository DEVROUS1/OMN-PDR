$(document).ready(function(){
	setInterval(function () {
		$('.uyari').removeClass('bg-dark');
	}, 1000);
	
	setInterval(function () {
		$('.uyari').addClass('bg-dark');
	}, 2000);
	
    $(".dogru").click(function(){
        if($(this).val() == "" || $(this).val() == undefined){
            $(this).val(0);
        }
        $(this).select();
    });
    $(".yanlis").click(function(){
        if($(this).val() == "" || $(this).val() == undefined){
            $(this).val(0);
        }
        $(this).select();
    });
    $(".dogru").change(function(){
        let dogruvalue = $(this).val();
        let yanlisvalue = $(this).closest("td").find(".yanlis").val();
        if(yanlisvalue == ""){
            yanlisvalue = 0;
            $(this).closest("td").find(".yanlis").val(0);
        }
        let netvalue = dogruvalue - (yanlisvalue/4);
        $(this).closest("td").find(".net").val(netvalue);
    });

    $(".yanlis").change(function(){
        let yanlisvalue = $(this).val();
        let dogruvalue = $(this).closest("td").find(".dogru").val();
        if(dogruvalue == ""){
            dogruvalue = 0;
            $(this).closest("td").find(".dogru").val(0);
        }
        let netvalue = dogruvalue - (yanlisvalue/4);
        $(this).closest("td").find(".net").val(netvalue);
    });

    $(".yks-temizle").click(function(){
        $(".tyt").find("input[type=number]").val("");
        $(".ayt").find("input[type=number]").val("");
    });

    //TYT-HESAPLAMA
    let current_year = $(".current-year").val(); 
    /*$("input[name=universiteye-yerlestim]").change(function(){
        let universiteyeyerlesme = $("input[name=universiteye-yerlestim]");
        let isyerlesme;
        if(universiteyeyerlesme[0].checked == true){
            isyerlesme = 1;
        }else{
            isyerlesme = 0;
        }

        let postname = "tyt-hesapla";
        let diplomapuani = $(".diploma-puani").val();
        if(diplomapuani == "" || diplomapuani < 0){
            diplomapuani = 0;
            $(".diploma-puani").val(0);
        }
        if(diplomapuani > 100){
            diplomapuani = 100;
            $(".diploma-puani").val(100);
        }

        let tytturkce = $(".tyt-t-net").val();
        if(tytturkce == ""){
            tytturkce = 0;
        }
        
        let tytsosyal = $(".tyt-s-net").val();
        if(tytsosyal == ""){
            tytsosyal = 0;
        }
        let tytmatematik = $(".tyt-m-net").val();
        if(tytmatematik == ""){
            tytmatematik = 0;
        }
        let tytfen = $(".tyt-f-net").val();
        if(tytfen == ""){
            tytfen = 0;
        }
        let aytmat = $(".ayt-mat-net").val();
        if(aytmat == ""){
            aytmat = 0;
        }
        let aytfizik = $(".ayt-fizik-net").val();
        if(aytfizik == ""){
            aytfizik = 0;
        }
        let aytkimya = $(".ayt-kimya-net").val();
        if(aytkimya == ""){
            aytkimya = 0;
        }
        let aytbiyoloji = $(".ayt-biyoloji-net").val();
        if(aytbiyoloji == ""){
            aytbiyoloji = 0;
        }
        let aytedebiyat = $(".ayt-edebiyat-net").val();
        if(aytedebiyat == ""){
            aytedebiyat = 0;
        }
        let ayttarih1 = $(".ayt-tarih1-net").val();
        if(ayttarih1 == ""){
            ayttarih1 = 0;
        }
        let aytcografya1 = $(".ayt-cografya1-net").val();
        if(aytcografya1 == ""){
            aytcografya1 = 0;
        }
        let ayttarih2 = $(".ayt-tarih2-net").val();
        if(ayttarih2 == ""){
            ayttarih2 = 0;
        }
        let aytcografya2 = $(".ayt-cografya2-net").val();
        if(aytcografya2 == ""){
            aytcografya2 = 0;
        }
        let aytfelsefe = $(".ayt-felsefe-net").val();
        if(aytfelsefe == ""){
            aytfelsefe = 0;
        }
        let aytdin = $(".ayt-din-net").val();
        if(aytdin == ""){
            aytdin = 0;
        }
        let aytdil = $(".ayt-dil-net").val();
        if(aytdil == ""){
            aytdil = 0;
        }

        //Send POST
        $(this).attr("disabled",true);
        $(this).css("cursor","progress");
        $.ajax({
            url: "hesapla.php",
            type: "post",
            data: {
                postname:postname,
                diplomapuani:diplomapuani,
                isyerlesme:isyerlesme,
                "tyt-t":tytturkce,
                "tyt-s":tytsosyal,
                "tyt-m":tytmatematik,
                "tyt-f":tytfen,
                "ayt-mat":aytmat,
                "ayt-fizik":aytfizik,
                "ayt-kimya":aytkimya,
                "ayt-biyoloji":aytbiyoloji,
                "ayt-edebiyat":aytedebiyat,
                "ayt-tarih1":ayttarih1,
                "ayt-cografya1":aytcografya1,
                "ayt-tarih2":ayttarih2,
                "ayt-cografya2":aytcografya2,
                "ayt-felsefe":aytfelsefe,
                "ayt-din":aytdin,
                "ayt-dil":aytdil
            },
            success: function(e){
                let response = JSON.parse(e);
                if(response[current_year] != undefined){
                    $(".tyt-ham-puan").val(response[current_year].ham);
                    $(".tyt-yerlestirme-puan").val(response[current_year].yerlestirme);
                    $(".ayt-ham-sayisal-puan").val(response[current_year]["sayisal-ham-puan"]);
                    $(".ayt-yerlestirme-sayisal-puan").val(response[current_year]["sayisal-yerlestirme-puan"]);
                    $(".ayt-ham-sozel-puan").val(response[current_year]["sozel-ham-puan"]);
                    $(".ayt-yerlestirme-sozel-puan").val(response[current_year]["sozel-yerlestirme-puan"]);
                    $(".ayt-ham-esit-puan").val(response[current_year]["esit-ham-puan"]);
                    $(".ayt-yerlestirme-esit-puan").val(response[current_year]["esit-yerlestirme-puan"]);
                    $(".ayt-ham-dil-puan").val(response[current_year]["dil-ham-puan"]);
                    $(".ayt-yerlestirme-dil-puan").val(response[current_year]["dil-yerlestirme-puan"]);
                }
                for(const [key,value] of Object.entries(response)){
                    $(".tyt-ham-siralama-"+key).val(value["tyt-ham-siralama"]);
                    $(".tyt-yerlestirme-siralama-"+key).val(value["tyt-yerlestirme-siralama"]);
                    $(".ayt-sayisal-ham-siralama-"+key).val(value["sayisal-ham-siralama"]);
                    $(".ayt-sayisal-yerlestirme-siralama-"+key).val(value["sayisal-yerlestirme-siralama"]);
                    $(".ayt-sozel-ham-siralama-"+key).val(value["sozel-ham-siralama"]);
                    $(".ayt-sozel-yerlestirme-siralama-"+key).val(value["sozel-yerlestirme-siralama"]);
                    $(".ayt-esit-ham-siralama-"+key).val(value["esit-ham-siralama"]);
                    $(".ayt-esit-yerlestirme-siralama-"+key).val(value["esit-yerlestirme-siralama"]);
                    $(".ayt-dil-ham-siralama-"+key).val(value["dil-ham-siralama"]);
                    $(".ayt-dil-yerlestirme-siralama-"+key).val(value["dil-yerlestirme-siralama"]);
                }  
            }
        });
        $(this).attr("disabled",false);
        $(this).css("cursor","pointer");
    });*/
    /*$('.yks-tyt').find("input[type=number]").change(function(){
        let universiteyeyerlesme = $("input[name=universiteye-yerlestim]");
        let isyerlesme;
        if(universiteyeyerlesme[0].checked == true){
            isyerlesme = 1;
        }else{
            isyerlesme = 0;
        }

        let postname = "tyt-hesapla";
        let diplomapuani = $(".diploma-puani").val();
        if(diplomapuani == "" || diplomapuani < 0){
            diplomapuani = 0;
            $(".diploma-puani").val(0);
        }
        if(diplomapuani > 100){
            diplomapuani = 100;
            $(".diploma-puani").val(100);
        }

        let tytturkce = $(".tyt-t-net").val();
        if(tytturkce == ""){
            tytturkce = 0;
        }
        
        let tytsosyal = $(".tyt-s-net").val();
        if(tytsosyal == ""){
            tytsosyal = 0;
        }
        let tytmatematik = $(".tyt-m-net").val();
        if(tytmatematik == ""){
            tytmatematik = 0;
        }
        let tytfen = $(".tyt-f-net").val();
        if(tytfen == ""){
            tytfen = 0;
        }
        let aytmat = $(".ayt-mat-net").val();
        if(aytmat == ""){
            aytmat = 0;
        }
        let aytfizik = $(".ayt-fizik-net").val();
        if(aytfizik == ""){
            aytfizik = 0;
        }
        let aytkimya = $(".ayt-kimya-net").val();
        if(aytkimya == ""){
            aytkimya = 0;
        }
        let aytbiyoloji = $(".ayt-biyoloji-net").val();
        if(aytbiyoloji == ""){
            aytbiyoloji = 0;
        }
        let aytedebiyat = $(".ayt-edebiyat-net").val();
        if(aytedebiyat == ""){
            aytedebiyat = 0;
        }
        let ayttarih1 = $(".ayt-tarih1-net").val();
        if(ayttarih1 == ""){
            ayttarih1 = 0;
        }
        let aytcografya1 = $(".ayt-cografya1-net").val();
        if(aytcografya1 == ""){
            aytcografya1 = 0;
        }
        let ayttarih2 = $(".ayt-tarih2-net").val();
        if(ayttarih2 == ""){
            ayttarih2 = 0;
        }
        let aytcografya2 = $(".ayt-cografya2-net").val();
        if(aytcografya2 == ""){
            aytcografya2 = 0;
        }
        let aytfelsefe = $(".ayt-felsefe-net").val();
        if(aytfelsefe == ""){
            aytfelsefe = 0;
        }
        let aytdin = $(".ayt-din-net").val();
        if(aytdin == ""){
            aytdin = 0;
        }
        let aytdil = $(".ayt-dil-net").val();
        if(aytdil == ""){
            aytdil = 0;
        }

        //Send POST
        $(this).attr("disabled",true);
        $(this).css("cursor","progress");
        $.ajax({
            url: "hesapla.php",
            type: "post",
            data: {
                postname:postname,
                diplomapuani:diplomapuani,
                isyerlesme:isyerlesme,
                "tyt-t":tytturkce,
                "tyt-s":tytsosyal,
                "tyt-m":tytmatematik,
                "tyt-f":tytfen,
                "ayt-mat":aytmat,
                "ayt-fizik":aytfizik,
                "ayt-kimya":aytkimya,
                "ayt-biyoloji":aytbiyoloji,
                "ayt-edebiyat":aytedebiyat,
                "ayt-tarih1":ayttarih1,
                "ayt-cografya1":aytcografya1,
                "ayt-tarih2":ayttarih2,
                "ayt-cografya2":aytcografya2,
                "ayt-felsefe":aytfelsefe,
                "ayt-din":aytdin,
                "ayt-dil":aytdil
            },
            success: function(e){
                let response = JSON.parse(e);
                if(response[current_year] != undefined){
                    $(".tyt-ham-puan").val(response[current_year].ham);
                    $(".tyt-yerlestirme-puan").val(response[current_year].yerlestirme);
                    $(".ayt-ham-sayisal-puan").val(response[current_year]["sayisal-ham-puan"]);
                    $(".ayt-yerlestirme-sayisal-puan").val(response[current_year]["sayisal-yerlestirme-puan"]);
                    $(".ayt-ham-sozel-puan").val(response[current_year]["sozel-ham-puan"]);
                    $(".ayt-yerlestirme-sozel-puan").val(response[current_year]["sozel-yerlestirme-puan"]);
                    $(".ayt-ham-esit-puan").val(response[current_year]["esit-ham-puan"]);
                    $(".ayt-yerlestirme-esit-puan").val(response[current_year]["esit-yerlestirme-puan"]);
                    $(".ayt-ham-dil-puan").val(response[current_year]["dil-ham-puan"]);
                    $(".ayt-yerlestirme-dil-puan").val(response[current_year]["dil-yerlestirme-puan"]);
                }
                for(const [key,value] of Object.entries(response)){
                    $(".tyt-ham-siralama-"+key).val(value["tyt-ham-siralama"]);
                    $(".tyt-yerlestirme-siralama-"+key).val(value["tyt-yerlestirme-siralama"]);
                    $(".ayt-sayisal-ham-siralama-"+key).val(value["sayisal-ham-siralama"]);
                    $(".ayt-sayisal-yerlestirme-siralama-"+key).val(value["sayisal-yerlestirme-siralama"]);
                    $(".ayt-sozel-ham-siralama-"+key).val(value["sozel-ham-siralama"]);
                    $(".ayt-sozel-yerlestirme-siralama-"+key).val(value["sozel-yerlestirme-siralama"]);
                    $(".ayt-esit-ham-siralama-"+key).val(value["esit-ham-siralama"]);
                    $(".ayt-esit-yerlestirme-siralama-"+key).val(value["esit-yerlestirme-siralama"]);
                    $(".ayt-dil-ham-siralama-"+key).val(value["dil-ham-siralama"]);
                    $(".ayt-dil-yerlestirme-siralama-"+key).val(value["dil-yerlestirme-siralama"]);
                }  
            }
        });
        $(this).attr("disabled",false);
        $(this).css("cursor","pointer");
    });*/
	
	//geçiçi butonla hesaplama yeri
	$('.btn-success').click(function(){
		let universiteyeyerlesme = $("input[name=universiteye-yerlestim]");
        let isyerlesme;
        if(universiteyeyerlesme[0].checked == true){
            isyerlesme = 1;
        }else{
            isyerlesme = 0;
        }

        let postname = "tyt-hesapla";
        let diplomapuani = $(".diploma-puani").val();
        if(diplomapuani == "" || diplomapuani < 0){
            diplomapuani = 0;
            $(".diploma-puani").val(0);
        }
        if(diplomapuani > 100){
            diplomapuani = 100;
            $(".diploma-puani").val(100);
        }

        let tytturkce = $(".tyt-t-net").val();
        if(tytturkce == ""){
            tytturkce = 0;
        }
        
        let tytsosyal = $(".tyt-s-net").val();
        if(tytsosyal == ""){
            tytsosyal = 0;
        }
        let tytmatematik = $(".tyt-m-net").val();
        if(tytmatematik == ""){
            tytmatematik = 0;
        }
        let tytfen = $(".tyt-f-net").val();
        if(tytfen == ""){
            tytfen = 0;
        }
        let aytmat = $(".ayt-mat-net").val();
        if(aytmat == ""){
            aytmat = 0;
        }
        let aytfizik = $(".ayt-fizik-net").val();
        if(aytfizik == ""){
            aytfizik = 0;
        }
        let aytkimya = $(".ayt-kimya-net").val();
        if(aytkimya == ""){
            aytkimya = 0;
        }
        let aytbiyoloji = $(".ayt-biyoloji-net").val();
        if(aytbiyoloji == ""){
            aytbiyoloji = 0;
        }
        let aytedebiyat = $(".ayt-edebiyat-net").val();
        if(aytedebiyat == ""){
            aytedebiyat = 0;
        }
        let ayttarih1 = $(".ayt-tarih1-net").val();
        if(ayttarih1 == ""){
            ayttarih1 = 0;
        }
        let aytcografya1 = $(".ayt-cografya1-net").val();
        if(aytcografya1 == ""){
            aytcografya1 = 0;
        }
        let ayttarih2 = $(".ayt-tarih2-net").val();
        if(ayttarih2 == ""){
            ayttarih2 = 0;
        }
        let aytcografya2 = $(".ayt-cografya2-net").val();
        if(aytcografya2 == ""){
            aytcografya2 = 0;
        }
        let aytfelsefe = $(".ayt-felsefe-net").val();
        if(aytfelsefe == ""){
            aytfelsefe = 0;
        }
        let aytdin = $(".ayt-din-net").val();
        if(aytdin == ""){
            aytdin = 0;
        }
        let aytdil = $(".ayt-dil-net").val();
        if(aytdil == ""){
            aytdil = 0;
        }
		$('.loader').removeClass('d-none');
        //Send POST
        $(this).attr("disabled",true);
        $(this).css("cursor","progress");
        $.ajax({
            url: "hesapla.php",
            type: "post",
            data: {
                postname:postname,
                diplomapuani:diplomapuani,
                isyerlesme:isyerlesme,
                "tyt-t":tytturkce,
                "tyt-s":tytsosyal,
                "tyt-m":tytmatematik,
                "tyt-f":tytfen,
                "ayt-mat":aytmat,
                "ayt-fizik":aytfizik,
                "ayt-kimya":aytkimya,
                "ayt-biyoloji":aytbiyoloji,
                "ayt-edebiyat":aytedebiyat,
                "ayt-tarih1":ayttarih1,
                "ayt-cografya1":aytcografya1,
                "ayt-tarih2":ayttarih2,
                "ayt-cografya2":aytcografya2,
                "ayt-felsefe":aytfelsefe,
                "ayt-din":aytdin,
                "ayt-dil":aytdil
            },
            success: function(e){
                let response = JSON.parse(e);
                if(response[current_year] != undefined){
                    $(".tyt-ham-puan").val(response[current_year].ham);
                    $(".tyt-yerlestirme-puan").val(response[current_year].yerlestirme);
                    $(".ayt-ham-sayisal-puan").val(response[current_year]["sayisal-ham-puan"]);
                    $(".ayt-yerlestirme-sayisal-puan").val(response[current_year]["sayisal-yerlestirme-puan"]);
                    $(".ayt-ham-sozel-puan").val(response[current_year]["sozel-ham-puan"]);
                    $(".ayt-yerlestirme-sozel-puan").val(response[current_year]["sozel-yerlestirme-puan"]);
                    $(".ayt-ham-esit-puan").val(response[current_year]["esit-ham-puan"]);
                    $(".ayt-yerlestirme-esit-puan").val(response[current_year]["esit-yerlestirme-puan"]);
                    $(".ayt-ham-dil-puan").val(response[current_year]["dil-ham-puan"]);
                    $(".ayt-yerlestirme-dil-puan").val(response[current_year]["dil-yerlestirme-puan"]);
                }
                for(const [key,value] of Object.entries(response)){
                    $(".tyt-ham-siralama-"+key).val(value["tyt-ham-siralama"]);
                    $(".tyt-yerlestirme-siralama-"+key).val(value["tyt-yerlestirme-siralama"]);
                    $(".ayt-sayisal-ham-siralama-"+key).val(value["sayisal-ham-siralama"]);
                    $(".ayt-sayisal-yerlestirme-siralama-"+key).val(value["sayisal-yerlestirme-siralama"]);
                    $(".ayt-sozel-ham-siralama-"+key).val(value["sozel-ham-siralama"]);
                    $(".ayt-sozel-yerlestirme-siralama-"+key).val(value["sozel-yerlestirme-siralama"]);
                    $(".ayt-esit-ham-siralama-"+key).val(value["esit-ham-siralama"]);
                    $(".ayt-esit-yerlestirme-siralama-"+key).val(value["esit-yerlestirme-siralama"]);
                    $(".ayt-dil-ham-siralama-"+key).val(value["dil-ham-siralama"]);
                    $(".ayt-dil-yerlestirme-siralama-"+key).val(value["dil-yerlestirme-siralama"]);
                }  
            },
        }).done(function(){
			$('.loader').addClass('d-none');
		});
        $(this).attr("disabled",false);
        $(this).css("cursor","pointer");
	});
	//sınavdan sonra bu kısım silinecek
	
    $('.kac-bin-geri-atar').find('input[type="number"]').click(function(){
        let value = $(this).val();
        if(value == ""){
            $(this).val(0); 
        }
        $(this).select();
    });

    $('.kac-bin-geri-atar').find('input[type="number"]').change(function(){
        let value = $(this).val();
        if(value < 0 ){
            $(this).val(0); 
        }
    });

    $('input[name="kac_bin_geri_atar_diploma_puani"]').change(function(){
        let value = $(this).val();
        if(value > 100){
            $(this).val(100); 
        }
    });

    $('.kac_bin_geri_atar_hesapla').click(function(){
        let kac_bin_geri_atar_tur = $('select[name="kac_bin_geri_atar_tur"]').val();
        let kac_bin_geri_atar_diploma_puani = $('input[name="kac_bin_geri_atar_diploma_puani"]').val();
        let kac_bin_geri_atar_check = $('input[name="kac_bin_geri_atar_check"]')[0].checked;
        let puan_veya_siralama = $('select[name="puan_veya_siralama"]').val();
        let puan_veya_siralama_input = $('input[name="puan_veya_siralama_input"]').val();

        $.ajax({
            url: "kac_bin_geri_atar_hesapla.php",
            type: "post",
            dataType: 'json',
            data: {
                tur:kac_bin_geri_atar_tur,
                diplomapuani:kac_bin_geri_atar_diploma_puani,
                check:kac_bin_geri_atar_check,
                puan_veya_siralama:puan_veya_siralama,
                puan_veya_siralama_input:puan_veya_siralama_input,
            },
            success:function(e){
                if(e.status == 1){
                    $('.kac_bin_geri_atar_answer').html(e.message);
                }
            }
        });
    });
})