This is a simple example of an MQTT pub/sub routine on a BuildHat (a LEGO PowerUp interface for the Raspberry Pi).
My BuildHat has a PU Button/Source Sensor for the Publish and a PU 3x3 LED Matrix as a Subscription indicator, but any cheaper PU LED can be used with some basic changes to the code.

This example assumes you have a MQTT broker running with a test/relay topic and the appropreate relay hardware.  However, again, any topic and/or hardware can be accommodated with adjustments to the code as needed.

The wonderfull assistance and code commenting was done by u/throwaway8u3sH0 on reddit here: https://www.reddit.com/r/pythonhelp/comments/1ht7wob/i_have_a_possible_syntax_or_layout_issue_with/
