$(window).load(function(){
    $('.dropdown-menu-equal-wd > li').each(function(){
        $(this).css({'width':$(this).parent().parent().width()});
    });


    $('#testAddForm').submit(function(e){
       if(!$.isNumeric($('#testprice').val())){
           e.preventDefault();
           $('#testprice').focus();
           $('#validation_error_add').css(
                {
                    'margin-left': '10%',
                    'margin-right': '10%',
                    'color':'black',
                }
           );
           $('#validation_error_add').fadeIn();
           $('#validation_error_add').find('div').html('Important ! The price should be a number, integer or decimal.');
           $('#validation_error_add').fadeOut(6000);
           return false;
       }
    });

    $('#patientAddForm').submit(function(e){
       $('#patientage').blur();
       $('#patientcontact').blur();
       if(!$.isNumeric($('#patientage').val())){
           e.preventDefault();
           $('#patientage').focus();
           $('#validation_error_add').css(
                {
                    'margin-left': '10%',
                    'margin-right': '10%',
                    'color':'black',
                }
           );
           $('#validation_error_add').fadeIn();
           $('#validation_error_add').find('div').html("Important ! Patient's age should be a number, integer or decimal.");
           $('#validation_error_add').fadeOut(6000);
           return false;
       }
       if(!$.isNumeric($('#patientcontact').val())){
           e.preventDefault();
           $('#patientcontact').focus();
           $('#validation_error_add').css(
                {
                    'margin-left': '10%',
                    'margin-right': '10%',
                    'color':'black',
                }
           );
           $('#validation_error_add').fadeIn();
           $('#validation_error_add').find('div').html("Important ! Patient's contact info should be a number.");
           $('#validation_error_add').fadeOut(6000);
           return false;
       }
    });


    $('.form-modify-tests').submit(function(e){
        if(!$.isNumeric($(this).find('input[name="testprice"]').val())){
            e.preventDefault();
            $(this).find('input[name="testprice"]').focus();
            $(this).find('#validation_error_modify').css(
                {
                    'margin-left': '10%',
                    'margin-right': '10%',
                    'color':'black',
                }
            );
            $(this).find('#validation_error_modify').fadeIn();
            $(this).find('#validation_error_modify').find('div').html('Important ! The price should be a number, integer or decimal.');
            $(this).find('#validation_error_modify').fadeOut(6000);
            return false;
        }
    });

    $('.form-modify-patients').submit(function(e){
        if(!$.isNumeric($(this).find('.patientcontact').val())){
            e.preventDefault();
            $(this).find('.patientcontact').focus();
            $(this).find('#validation_error_modify').css(
                {
                    'margin-left': '10%',
                    'margin-right': '10%',
                    'color':'black',
                }
            );
            $(this).find('#validation_error_modify').fadeIn();
            $(this).find('#validation_error_modify').find('div').html("Important ! Patient's contact info should be a number.");
            $(this).find('#validation_error_modify').fadeOut(6000);
            return false;
        }

        if(!$.isNumeric($(this).find('.patientage').val())){
            e.preventDefault();
            $(this).find('.patientage').focus();
            $(this).find('#validation_error_modify').css(
                {
                    'margin-left': '10%',
                    'margin-right': '10%',
                    'color':'black',
                }
            );
            $(this).find('#validation_error_modify').fadeIn();
            $(this).find('#validation_error_modify').find('div').html("Important ! Patient's age should be a number, integer or decimal.");
            $(this).find('#validation_error_modify').fadeOut(6000);
            return false;
        }

    });


    $('#userAddForm').submit(function(){
       if($('#userAddForm input:checked').length === 0){
           $('.required-info').css({'color':'red','font-weight':'bold'});
           return false;
       }
    });

    $('#roleAddForm').submit(function(){
       if($('#roleAddForm input:checked').length === 0 ){
           $('.required-info').css({'color':'red','font-weight':'bold'});
           return false;
       }
    });

    $('.test-region').find('.row:lt(1)').addClass('active');
    $('.test-region').find('.row:last').addClass('active');
    $('.more-button-test').click( function(){
        $(this).text(function(i, v){
            return v === 'More ...' ? 'Less ...' : 'More ...'
        });
        var $current = $(this).closest('.test-region');
        var pos = $current.offset();
        $current.find('.row').not('.active').not('.more-row').toggle('slow');
        $('body').animate({scrollTop: pos.top - 60});
    });

    $('.patient-region').find('.row:lt(1)').addClass('active');
    $('.patient-region').find('.row:last').addClass('active');
    $('.more-button-patient').click( function(){
        $(this).text(function(i, v){
            return v === 'More ...' ? 'Less ...' : 'More ...'
        });
        var $current = $(this).closest('.patient-region');
        var pos = $current.offset();
        $current.find('.row').not('.active').not('.more-row').toggle('slow');
        $('body').animate({scrollTop: pos.top - 60 });
    });


    $('.search-role-input').on('keyup',function(){
        var $that = $(this);
        if($(this).val()===''){
            $('.no-result-msg').addClass('inactive');
            $('.form-role').removeClass('inactive');
        }
        else{
            $('.form-role').addClass('inactive');
            var count = 0;
            $('.role-name').each(function(){
                var str1 = $(this).text().toLowerCase();
                if(str1.indexOf($that.val().toLowerCase()) >= 0){
                    count++;
                    $(this).closest('.form-role').removeClass('inactive');
                }
            });
            if(count === 0){
                $('.no-result-msg').removeClass('inactive');
            }
            else{
                $('.no-result-msg').addClass('inactive');
            }
        }
    });

    $('.search-user-input').on('keyup',function(){
        var $that = $(this);
        if($(this).val()===''){
            $('.no-result-msg').addClass('inactive');
            $('.usersinfo').removeClass('inactive');
        }
        else{
            $('.usersinfo').addClass('inactive');
            var count = 0;
            $('.usernameholder').each(function(){
                var str1 = $(this).val().toLowerCase();
                if(str1.indexOf($that.val().toLowerCase()) >= 0){
                    count++;
                    $(this).closest('.usersinfo').removeClass('inactive');
                }
            });
            if(count === 0){
                $('.no-result-msg').removeClass('inactive');
            }
            else{
                $('.no-result-msg').addClass('inactive');
            }
        }
    });

    $('.search-test-input').on('keyup',function(){
        var $that = $(this);
        if($(this).val()===''){
            $('.no-result-msg').addClass('inactive');
            $('.test-region').removeClass('inactive');
        }
        else{
            $('.test-region').addClass('inactive');
            var count = 0;
            $('.test-region').find('input').each(function(){
                var str1 = $(this).val().toLowerCase();
                if(str1.indexOf($that.val().toLowerCase()) >= 0){
                    count++;
                    $(this).closest('.test-region').removeClass('inactive');
                }
            });
            if(count === 0){
                $('.no-result-msg').removeClass('inactive');
            }
            else{
                $('.no-result-msg').addClass('inactive');
            }
        }
    });


    $('.search-patient-input').on('keyup',function(){
        var $that = $(this);
        if($(this).val()===''){
            $('.no-result-msg').addClass('inactive');
            $('.patient-region').removeClass('inactive');
        }
        else{
            $('.patient-region').addClass('inactive');
            var count = 0;
            $('.patient-region').find('input').each(function(){
                var str1 = $(this).val().toLowerCase();
                if(str1.indexOf($that.val().toLowerCase()) >= 0){
                    count++;
                    $(this).closest('.patient-region').removeClass('inactive');
                }
            });
            if(count === 0){
                $('.no-result-msg').removeClass('inactive');
            }
            else{
                $('.no-result-msg').addClass('inactive');
            }
        }
    });

    $('.form-modify-tests').find('.checkbox-md').each(function(){
        if($(this).val() === '0'){
            $(this).prop('checked',false);
        }
        else{
            $(this).prop('checked',true);
        }
    });

    $('.form-modify-users').find('button[type="submit"]').on("click",function(){
        $(this).attr("clicked","true");
    });

    $('.form-role').find('button[type="submit"]').on("click",function(){
        $(this).attr("clicked","true");
    });

    $('.form-modify-users').submit( function(e){
        if($(this).find("button[type=submit][clicked=true]").val() == 'save'){
            if($(this).find('input:checked').length === 0){
                e.preventDefault();
                $('.alert-danger').css(
                    {
                        'position': 'fixed',
                        'width':'50%',
                        'top': '8.5%',
                        'left': '25%',
                    }
                );
                $('.alert-danger').fadeIn('slow');
                $('.alert-danger').fadeOut(7000);
                return false;
            }
        }
        $('button[type="submit"]').removeAttr('clicked');
    });

    $('.form-role').submit( function(e){
        if($(this).find("button[type=submit][clicked=true]").val() == 'save'){
            if($(this).find('input:checked').length === 0){
                e.preventDefault();
                $('.alert-danger').css(
                    {
                        'position': 'fixed',
                        'width':'50%',
                        'top': '8.5%',
                        'left': '25%',
                    }
                )
                $('.alert-danger').fadeIn('slow');
                $('.alert-danger').fadeOut(7000);
                return false;
            }
        }
        $('button[type="submit"]').removeAttr('clicked');
    });



    $('.form-modify-tests').find('input[type="checkbox"]').on("change",function(){
        if($(this).prop('checked')){
            $(this).val(1);
        }
        else{
            $(this).val(0);
        }
    });

    $('.incorrect').addClass('active');

    $('input[name="confirmpasswd"]').on('keyup',function(){
        if($(this).val() === $('input[name="newpasswd"]').val()){
            $('.correct').addClass('active');
            $('.incorrect').removeClass('active');
        }
        else{
            $('.incorrect').addClass('active');
            $('.correct').removeClass('active');
        }
    });
});



