#!/usr/bin/perl -w
#http://www.cs.utexas.edu/~stormy12/CS105/DNAdatabase.cgi
use warnings;
use strict;
use Email::Valid;
use CGI;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);

my $q = CGI->new;

                  #start html page

                  print $q->header,
                        $q->body,
                        $q->start_html(-title=>'DNA Sequence Database',
	                               -author=>'stormyemery12@utexas.edu',
		                       -style=>{-src=>'DNAcss.css'},
	                ),
                        $q->div({-class=>'wrapper'});

                  print $q->div({-class=> 'header'}, $q->img({-src=> 'DNA1.gif', -class=> 'align-left'}),
		                         	     $q->img({-src=> 'DNA1.gif', -class=> 'align-right'}),
				                     $q->a({-class=>'title', -href=>'http://www.cs.utexas.edu/~stormy12/CS105/DNAdatabase.cgi', 
				                            -title=> 'Home'},
				   	                    $q->div({-class=> 'title'},
				          	            'DNA Sequence Database',
					                    ),
				                      ),
			$q->hr({-class=>'one'}),
				    
	         );




#####################################################
#                    ADD SEQUENCE                   # 
# form to accept name of a sequence                 #
# and the dna sequence                              #
##################################################### 
	     
                  print $q->start_div({-class=>'form_one'}); 
                  print $q->p({-class=>'title'}, "Would you like to add a sequence to the database?"),
			$q->hr({-class=>'two'}),
			$q->start_form({-class=>'first_form'}),
			$q->label({-class=>'label_one'}, 'Enter the name of your sequence:'),
		        $q->br,
			$q->textfield(-name=>'name',
				      -class=>'inside1'),
			$q->br,
			$q->label({-class=>'label_one'}, 'Enter your sequence here:'),
			$q->br,
		        $q->textarea(-name=>'sequence',
				     -class=>'inside2'),
			$q->br,
			$q->submit(-name=>'add',
			           -value=>'Add Your Sequence',
			           -class=>'reset'),
			$q->end_form;



                  # getting values from text fields

		  my $name = $q->param('name');
		  my $sequence = lc($q->param('sequence'));
		  my $submit = $q->param('add');
		  my $switch = 0;




                                                 
                  # determines whether user given name is 
                  # already in the database and determines
                  # whether the user given name is whitespace
                  # if either of these conditions hold true,
                  # a flag is set and that user given information
                  # will not be written to the database


		  if($name && $sequence) {
		        open(my $fh, '<', 'data.txt');
			my $file_name;
						 		
                        while(my $line = <$fh>) {
			      chomp($line);
			      my @seq = split (',',$line);
			      $file_name = shift(@seq);
                              
			      if($name eq $file_name) {
				    print $q->p({-class=>'form_one_noname'}, 
				                 "A sequence with that name already exist...");
				    $switch = 1;
				    last;
			      }
			      elsif($name=~/\s+/g) {
				    print $q->p({-class=>'form_one_noname'}, 
						 "Whitespace is not a valid name for a sequence...");
				    $switch = 1;
			            last;
			      }
			}
			close $fh;


                        #lets the user know that his/her sequence has been
                        #successfully added to the database

			if(($name ne $file_name) && ($name=~/[^\s]+/g)) {
			      print $q->p({-class=>'form_one'}, 'Successfully added sequence', 
				    $q->span({-class=> 'italics'}, $name), 'to database!');
			}
		  }

                  
                  
                  # Tells the user that they need to enter a sequence 
                  # not written to database

		  elsif($name && !$sequence && $submit) {
			print $q->p({-class=>'form_one_nosequence'}, "Please enter a sequence!");
		  }


                  # Tells the user that they need to enter a name
                  # not written to database

		  elsif($sequence && !$name && $submit) {
			print $q->p({-class=>'form_one_noname'}, "Please enter a name for your sequence!");
		  }

                  
                  # Tells the user that they need to enter
                  # a name and a sequence
                  # not written to database

		  elsif(!$sequence && !$name && $submit) {
			print $q->p({-class=>'form_one_noname'}, "Please enter a name and a sequence!");
		  
                }

                  #end of div element
                  print $q->end_div();
	    



                  # writes the name of the sequence
                  # and the sequence itself to a text file
                  # if the variable $switch is 0

                  if($name && $sequence && $submit) {
	                my $new_sequence = "";
	                open(my $fh, '>>','data.txt');
	                my @chars = split ("\n", $sequence);
	                foreach my $char(@chars) {
		              $new_sequence .= $char;
	                }
	                if($switch == 0) {
		              print $fh "$name,$new_sequence\n";
	                }
	                close $fh;
                  }




#####################################################
#               SEARCH SEQUENCE                     # 
# starts form to search for                         #
# specific sequences or everything                  #
# that is in the database                           #
#####################################################
                  

                  print $q->br,
                        $q->br;
      

                  # starts form for searching the database

                  print $q->start_div({-class=>'form_two'}); 
                  print $q->p({-class=>'title'}, "Would you like to search for a specific sequence? \n (Leave unused fields blank)"),
			$q->hr({-class=>'two'}),
		    	$q->start_form({-class=>'first_form'}),
		    	$q->label({-class=>'label_one'}, 'Name of Sequence:'),
		    	$q->br,
		    	$q->textfield(-name=>'search_name',
			    	      -class=>'search1'),
		    	$q->br,
		        $q->label({-class=>'label_one'}, 'Desired Sequence:'),
		    	$q->br,
		    	$q->textarea(-name=>'search_sequence',
			    	     -class=>'search2'),
			$q->br,
			$q->br,
		    	$q->label({-class=>'label_one'}, 'Provide an email address to recieve the search results:'),
		        $q->br,
		        $q->textfield(-name=> 'email',
			      	      -class=> 'email_results',
				      -type=>'email',
				      -placeholder=>'me@example.com'),
			$q->br,
			$q->submit(-name=>'search',
				   -value=>'Search',
			           -class=>'reset'),
			$q->end_form;



                        # getting values from text fields

			my $seq_name = lc($q->param('search_name'));
			my $seq_chars = lc($q->param('search_sequence'));
		        my $email = $q->param('email');
			my $submit_search = $q->param('search');
			my $email_message = "Results:\n\n";
			my $switch = 0;



			# returns results of searching
                        # for nothing, a name, a sequence,
                        # or a name and a sequence
                        # also emails the results to the user
                        # if they specify a valid email


			
		        # handles when both text fields are empty
            
			if(!$seq_name && !$seq_chars && $submit_search) {
			      open(my $fh, '<', 'data.txt');

                              # this checks to see if the database is empty
                              # if it is, it notifies the user
			      if(-z 'data.txt') {
				    print $q->p({-class=>'form_one_noname'}, "The database is empty...");
			      }
			      else {
				    print $q->p({-class=>'results_title'}, 'Results:');
			            print $q->start_div({-class=>'rslts'});
				    my $name;
			            my $seq;

				    while(my $line = <$fh>) {
				          chomp($line);
				          my @seq = split (',',$line);
					  $name = shift(@seq);
				          $seq = shift(@seq);
					  $seq =~s/\s+//g;
				          
                                          print $q->div({-class=>'contain'},
					        $q->p({-class=>'results_name'}, "> $name"),
						$q->p({-class=>'results_seq'}, "$seq")
						);


					  #this concatenates the name and sequence
                                          #from this search onto a string
                                          #which will be used to email to the user
                                          #if they want the results emailed
                                          $email_message .= "> $name\n\t$seq\n";
				    }

				    print $q->end_div();
			      }

		              close $fh;
		        }



      			#just name field is filled

			elsif($seq_name && !$seq_chars && $submit_search) {
			      open(my $fh, '<', 'data.txt');
			      if(-z 'data.txt') {
				    print $q->p({-class=>'form_one_noname'}, "The database is empty...");
			      }
			      else {
				    print $q->p({-class=>'results_title'}, 'Results:');
				    print $q->start_div({-class=>'rslts'});
				    my $name;
				    my $seq;
				    
                                    while(my $line = <$fh>) {
					  chomp($line);
					  my @seq = split (',',$line);
				          $name = shift(@seq);
					  $seq = shift(@seq);
					  $seq =~s/\s+//g;
					  
                                          if(index(lc($name), lc($seq_name)) != -1) {
						print $q->div({-class=>'contain'},
						      $q->p({-class=>'results_name'}, "> $name"),
						      $q->p({-class=>'results_seq'}, "$seq")
						      );

						$email_message .= "> $name\n\t$seq\n"; 
					  }
				    }

				    print $q->end_div();
			      }

			      close $fh;
			}
				


			# just seq field is filled
                        # same concept as above

			elsif(!$seq_name && $seq_chars && $submit_search) {
			      open(my $fh, '<', 'data.txt');
			      if(-z 'data.txt') {
			            print $q->p({-class=>'form_one_noname'}, "The database is empty...");
			      }
			      else {
				    print $q->p({-class=>'results_title'}, 'Results:');
			            print $q->start_div({-class=>'rslts'});
				    my $name;
				    my $seq;
				    
                                    while(my $line = <$fh>) {
					  chomp($line);
				          my @seq = split (',',$line);
					  $name = shift(@seq);
					  $seq = shift(@seq);
					  $seq =~s/\s+//g;
					  
                                          if(index($seq, $seq_chars) != -1) {
						print $q->div({-class=>'contain'},
						      $q->p({-class=>'results_name'}, "> $name"),
						      $q->p({-class=>'results_seq'}, "$seq")
						      );
						
                                                $email_message .= "> $name\n\t$seq\n"; 
					  }
				    }

				    print $q->end_div();
			      }

			      close $fh;
			}
			


			# both fields are filled
                        # same concept as above

			elsif($seq_name && $seq_chars && $submit_search) {
			      open(my $fh, '<', 'data.txt');
			      if(-z 'data.txt') {
				    print $q->p({-class=>'form_one_noname'}, "The database is empty...");
			      }
			      else {
			            print $q->p({-class=>'results_title'}, 'Results:');
				    print $q->start_div({-class=>'rslts'});
				    my $name;
				    my $seq;
				    
                                    while(my $line = <$fh>) {
					  chomp($line);
					  my @seq = split (',',$line);
					  $name = shift(@seq);
					  $seq = shift(@seq);
					  $seq =~s/\s+//g;
					  
                                          if((index($seq, $seq_chars) != -1) && (index(lc($name), lc($seq_name)) != -1)) {
						print $q->div({-class=>'contain'},
						      $q->p({-class=>'results_name'}, "> $name"),
						      $q->p({-class=>'results_seq'}, "$seq")
						      );
						$email_message .= "> $name\n\t$seq\n"; 
					  }
			            }

				    print $q->end_div();
			      }

			      close $fh;
			}


      			# emails the results to user
			# if the email is valid
						
		  	if($email && $submit_search) {

                              # this checks to make sure the email is valid
                              # if valid ...
			      if(Email::Valid->address(-address=>$email, -tldcheck=> 1)) {
				    $switch = 1;
			      }

                              # if email is valid
			      if($switch == 1) {
				    my $to = $email;
				    my $from = 'stormyemery12@utexas.edu';
				    my $subject = 'DNA Search Results';

				    open(MAIL, "|/usr/sbin/sendmail -t");
	
				    # email header
				    print MAIL "To: $to\n";
				    print MAIL "From: $from\n";
			            print MAIL "Subject: $subject\n\n";

			            # email body
				    print MAIL $email_message;
	
				    close(MAIL);
				    print $q->p({-class=>'form_one'}, 'Email sent successfully!');
			      }

                              # email is not valid
                              # notifies user
                              # doesn't try to send
			      elsif($switch == 0) {
				    print $q->p({-class=>'form_one_noname'}, "Not a valid email, try again...");
			      }
			}

#####################################################
#               CLEAR DATABASE                      # 
# Clears the database                               #
#####################################################
                        
      
                        print $q->end_div(),
                        $q->br,
                        $q->br;

                        # clears the database on button click
                        print $q->start_div({-class=>'form_one'}); 
                        print $q->p({-class=>'title'}, "Would you like to clear the database?"),
			      $q->hr({-class=>'two'}),
			      $q->start_form({-class=>'first_form'}),
			      $q->submit(-name=>'reset',
				         -value=>'Clear',
				         -class=>'reset2'),
			      $q->end_form;

			      my $submit = $q->param('reset');

			      if($submit) {
                                    # this clears the file
			            open(my $fh, '>', 'data.txt');

				    print $q->p({-class=>'title2'}, 'Database Cleared!');
			      }

                        print $q->end_div(),
                              $q->br;

                        # copyright
                        print $q->p({-class=>'copyright'}, "&copy Copyright Stormy Emery 2014");

                        
                        # end of page
                        print $q->end_html;








