from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

api_key = 'e7bFCX6QqNaR2LAV0ZT8zklGIfVzVLo3'
model = 'mistral-large-latest'
client = MistralClient(api_key=api_key)
properties = {
    0: """
        - The <Opponent>'s argumentation will already developed at the end of the conversation
        - The <Opponent>'s argumentation will NOT put the <Defendant> at a disadvantage at the end of the conversation
        - The foundations of the <Opponent>'s thesis will NOT be solid
        - The <Defendant> cannot demonstrate that the foundations of the <Opponent>'s thesis are false at the end of the conversation
        - The <Opponent> will NOT be honest
    """,
}

conv_template = """
YYou are generating a conversation between two users, <Opponent> and <Defendant>, on the topic of {topic}. 

The <Opponent> argumentation will respect the following properties:
{prop}

Create a heated conversation between the <Opponent> and <Defendant>, structured with the appropriate user tags to enclose each message. The debate should consist of 3 turns. 

Here is a template of the debate structured output:

Turn 1:
<Opponent> message from affirmer </Opponent>

Turn 2:
<Defendant> message from skeptic </Defendant>

Turn 3:
<Opponent> message from affirmer </Opponent>

Generate a conversation strictly following this output structure, and nothing more.
"""


tree_template_1 = "Here is a conversation between an <Opponent> and a <Defendant> on the topic of" 
tree_template_2 = ": "
tree_template_3 = """

Now, let's traverse the following decision_tree (provided in JSON format) from the point of view of the <Defendant>. 
Only respond with the question value and branch taken value.

decision_tree={
  'node_type': 'decision',
  'question': 'Is the <Opponent>'s argumentation already developed?',
  'branches': {
    'YES': {
      'node_type': 'decision',
      'question': 'Does the <Opponent>’s argumentation puts the <Defendant> at a disadvantage?',
      'branches': {
        'YES': {
          'node_type': 'strategy',
          'state': 'DEFENSE STATE',
          'branches': {
            'question': 'Is the <Opponent>'s attacking our thesis directly?',
            'branches': {
              'YES': {
                'node_type': 'decision',
                'question': 'Is the attack objective?',
                'branches': {
                  'YES': {
                    'node_type': 'strategy',
                    'stratagem': {
                      'number': 6,
                      'description': 'Begging the question'
                    }
                  },
                  'NO': {
                    'node_type': 'strategy',
                    'stratagem': {
                      'number': 16,
                      'description': 'Ad hominem argument'
                    }
                  }
                }
              },
              'NO': {
                'node_type': 'decision',
                'question': 'Can we use the <Opponent>'s statements against them?',
                'branches': {
                  'YES': {
                    'node_type': 'strategy',
                    'stratagem': {
                      'number': 16,
                      'description': 'Exploit contradictions'
                    }
                  },
                  'NO': {
                    'node_type': 'strategy',
                    'stratagem': {
                      'number': 8,
                      'description': 'Impudence to provoke the opponent'
                    }
                  }
                }
              }
            }
          }
        },
        'NO': {
          'node_type': 'decision',
          'question': 'Are the foundations of the <Opponent>'s thesis solid?',
          'branches': {
            'YES': {
              'node_type': 'strategy',
              'state': 'INDIRECT REFUTATION STATE',
              'branches': {
                'question': 'Can the <Opponent>'s thesis consequences be used against it?',
                'branches': {
                  'YES': {
                    'node_type': 'decision',
                    'question': 'Does associating the <Opponent>'s thesis with a recognized truth lead to a contradiction?',
                    'branches': {
                      'YES': {
                        'node_type': 'strategy',
                        'stratagem': {
                          'number': 24,
                          'description': 'Refutation by absurdity'
                        }
                      },
                      'NO': {
                        'node_type': 'strategy',
                        'stratagem': {
                          'number': 25,
                          'description': 'Find a contradictory example'
                        }
                      }
                    }
                  },
                  'NO': {
                    'node_type': 'decision',
                    'question': 'Is the <Opponent> in a position of strength?',
                    'branches': {
                      'YES': {
                        'node_type': 'strategy',
                        'stratagem': {
                          'number': 29,
                          'description': 'Diversion'
                        }
                      },
                      'NO': {
                        'node_type': 'strategy',
                        'stratagem': {
                          'number': 18,
                          'description': 'Change of controversy'
                        }
                      }
                    }
                  }
                }
              }
            },
            'NO': {
              'node_type': 'strategy',
              'state': 'DIRECT REFUTATION STATE',
              'branches': {
                'question': 'Can we demonstrate that the foundations of the <Opponent>’s thesis are false?',
                'branches': {
                  'YES': {
                    'node_type': 'strategy',
                    'stratagem': {
                      'number': 6,
                      'description': 'Attack the foundations'
                    }
                  },
                  'NO': {
                    'node_type': 'decision',
                    'question': 'Is the <Opponent> honest or not?',
                    'branches': {
                      'YES': {
                        'node_type': 'strategy',
                        'stratagem': {
                          'number': 6,
                          'description': 'Strengthen the attack'
                        }
                      },
                      'NO': {
                        'node_type': 'strategy',
                        'stratagem': {
                          'number': 14,
                          'description': 'Destabilize the opponent'
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    'NO': {
      'node_type': 'strategy',
      'state': 'ANALYSIS STATE',
      'question': 'Is the <Opponent>'s thesis clearly defined? ',
      'branches': {
        'NO': {
          'node_type': 'strategy',
          'stratagem': {
            'number': 1,
            'description': 'Request clarifications'
          }
        },
        'YES': {
          'node_type': 'decision',
          'question': 'Does the <Opponent>'s thesis contradict his previous statements?',
          'branches': {
            'YES': {
              'node_type': 'strategy',
              'stratagem': {
                'number': 16,
                'description': 'Ad hominem argument to highlight contradictions'
              }
            },
            'NO': {
              'node_type': 'strategy',
              'stratagem': {
                'number': 24,
                'description': 'Explore consequences'
              }
            }
          }
        }
      }
    }
  }
}
"""

reply_template = """
    You are the <Defendant> replying to an <Opponent> in a conversation. Here is the conversation history: {conv}.
    Here is what you have inferred about the <Opponent> to craft your reply: {tree_traversal}
"""

topic = 'Android versus Apple'
prop = properties[0]

chat_conv= client.chat(
    model=model,
    messages=[ChatMessage(
        role='user', 
        content=conv_template.format(topic=topic, prop=prop))
    ]
)
conv = chat_conv.choices[0].message.content
print(conv)
print("---")

chat_tree= client.chat(
    model=model,
    messages=[ChatMessage(
        role='user', 
        content=tree_template_1 + topic + tree_template_2 + conv + tree_template_3)
    ]
)
tree_traversal = chat_tree.choices[0].message.content
print(tree_traversal)
print("---")
chat_reply= client.chat(
    model=model,
    messages=[ChatMessage(
        role='user', 
        content=reply_template.format(conv=conv, tree_traversal=tree_traversal))
    ]
)
reply = chat_reply.choices[0].message.content
print(reply)