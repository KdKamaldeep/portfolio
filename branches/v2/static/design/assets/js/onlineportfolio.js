$(function () {

    $('*[data-poload]')
        .webuiPopover({
            type:'async',
            trigger:'hover',
            width:800,
            container: document.body
        });

    $('.datepicker').datepicker({
        format: 'dd-mm-yyyy',
        startDate: '-3d'
    });

    $(document).ready(function(){
        $('[data-toggle="tooltip"]').tooltip();
    });

    $('.anchorremove').bind('click', function (e) {
        if(!window.confirm('Are you sure?'))
        {
            e.preventDefault();
        }
    });

    $(document).delegate('*[data-toggle="lightbox"]', 'click', function(event) {
        event.preventDefault();
        return $(this).ekkoLightbox({
            always_show_close: true
        });
    });

    $(document).mouseup(function (e)
    {
        var container = $(".notificationcontainer");
        if (!container.is(e.target)
            && container.has(e.target).length === 0)
        {
            container.hide();
        }
    });

    function marknotification_as_read() {
        $.get('/public/mark_as_read',function () {
            $('.badgenotifictioan').remove()
        })
    }

    $('.notificationlink').bind('click', function () {
        var current = $(this);
        var mark_as_read = current.attr('mark_as_read')
        var container = current.next('.notificationcontainer')
        container.show()
        if(mark_as_read=="yes") {
            marknotification_as_read()
        }
    });

    $('.closenotify').bind('click', function () {
        $(this).parents('.datanotifycontainer').hide()
    })

    //It reside in /base/portfolio-header.html file too.  Bcoz we are using it in popups
    // so single script woulbe be registerd twice so to overcome it I duplicate this code as well.
    function  acceptreject(contactid, status) {
        $.get('/public/accept_reject_contact_request/' + contactid + '/' + status, function () {
            window.location = '/account/contacts/'
        })
    };

    //It reside in /base/portfolio-header.html file too.  Bcoz we are using it in popups
    // so single script woulbe be registerd twice so to overcome it I duplicate this code as well.
    $('.acceptrejectbutton').unbind('click')
    $('.acceptrejectbutton').bind('click', function () {
        var self = $(this);
        var message = $('.message')
        var container = $('.datanotifycontainer')
        var action = self.attr('requestaction')
        var contactid = self.attr('contact-id')
        if (action == "accept"){
            acceptreject(contactid, 'ACCEPTED')
            message.empty()
            message.html('You have accepted the contact request.')
            container.show()

        }
        else {
            acceptreject(contactid, 'REJECTED')
            message.empty()
            message.html('You have rejected the contact request.')
            container.show()
        }
    })

    //It reside in /base/portfolio-header.html file too.  Bcoz we are using it in popups
    // so single script woulbe be registerd twice so to overcome it I duplicate this code as well.
    $('.contactrequestbutton').unbind('click')
    $('.contactrequestbutton').bind('click', function () {
        div = $('.infomessage');
        var self = $(this)
        var image = $('<img />')
                .attr({'src':'/static/design/assets/img/loading.gif',
                'style':'width: 15px;height: auto;margin-right: 8px;margin-left: 2px;margin-top: -2px;'})

        var tocontactid = self.attr('to-contact-id')
        var fromcontactid = self.attr('from-contact-id')
        if(div.length>0){
            div.show()
        }
        else
        {
            self.find('img').remove()
            self.append(image)
            self.attr('disabled','disabled')
            $.get('/public/send_contact_request/'+ tocontactid, function () {
                self.empty()
                self.html('<i class="fa fa-check" aria-hidden="true"></i> Contact request sent')
            })
        }
    })
});