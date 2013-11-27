jQuery(function() {

    function toggle_birth_date(number) {
        if (number > 0) {
            $("input[name='birth_date']").removeAttr('required');
            $(".birth_date").css('display', 'none');
        } else {
            $("input[name='birth_date']").attr('required');
            $(".birth_date").css('display', 'block');
        }
    }

    $("input[name='birth_date']").prop('type', 'text');

    var billing_organization = $("input[name='billing_organization']").val();
    if (billing_organization) {
        var organization = billing_organization.trim();
        var number = organization.length;
        toggle_birth_date(number);
    }

    $("#content-core").on("change", "input[name='billing_organization']", function(event) {
        var organization = this.value.trim();
        var number = organization.length;
        toggle_birth_date(number);
    });

});