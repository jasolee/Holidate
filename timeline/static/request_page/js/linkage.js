(function($){
    /**
     * jQuery.fn.dependsOn
     * @version 1.0.1
     * @date September 22, 2010
     * @since 1.0.0, September 19, 2010
     * @package jquery-sparkle {@link http://www.balupton/projects/jquery-sparkle}
     * @author Benjamin "balupton" Lupton {@link http://www.balupton.com}
     * @copyright (c) 2010 Benjamin Arthur Lupton {@link http://www.balupton.com}
     * @license Attribution-ShareAlike 2.5 Generic {@link http://creativecommons.org/licenses/by-sa/2.5/
     */
    $.fn.dependsOn = function(source,value){
        var $target = $(this),
            $source = $(source),
            source = $source.attr('name')||$source.attr('id');
    
        // Add Data
        var dependsOnStatus = $target.data('dependsOnStatus')||{};
        dependsOnStatus[source] = false;
        $target.data('dependsOnStatus',dependsOnStatus);
        
        // Add Event
        $source.change(function(){
            var pass = false;
            var $source = $(this); // so $source won't be a group for radios
        
            // Determine
            if ( (value === null) || (typeof value === 'undefined') ) {
                // We don't have a value
                if ( $source.is(':checkbox,:radio') ) {
                    pass = $source.is(':selected:enabled,:checked:enabled');
                }
                else {
                    pass = Boolean($source.val());
                }
            }
            else {
                // We do have a value
                if ( $source.is(':checkbox,:radio') ) {
                    pass = $source.is(':selected:enabled,:checked:enabled') && ($source.val() == value);
                }
                else {
                    pass = $source.val() == value;
                }
            }
        
            // Update
            var dependsOnStatus = $target.data('dependsOnStatus')||{};
            dependsOnStatus[source] = pass;
            $target.data('dependsOnStatus',dependsOnStatus);
        
            // Determine
            var passAll = true;
            $.each(dependsOnStatus, function(i,v){
                if ( !v ) {
                    passAll = false;
                    return false; // break
                }
            });
            // console.log(dependsOnStatus);
        
            // Adjust
            if ( !passAll ) {
                $target.attr('disabled','disabled').addClass('disabled');
            }
            else {
                $target.removeAttr('disabled').removeClass('disabled');
            }
        }).trigger('change');
        
        // Chain
        return this;
    };

    $(function(){
        $('#foo').dependsOn('#boo').dependsOn('#moo','test')
            .dependsOn(":radio[name=doo]",'true');
    });

    $(function(){
        $('#end_date').dependsOn('#halfday_setting','F');
    });

})(jQuery);