/**
  ******************************************************************************
  * File Name          : command.c
  * Description        : This file provides code for the interpretation of 
  *                      protobuf messages.
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "proto_handler.h"

/* Private typedef -----------------------------------------------------------*/

/* Private define ------------------------------------------------------------*/
#define MAX_MESSAGE_LENGTH 0x400U // A fairly arbitrary value of 1024

/* Private variables ---------------------------------------------------------*/

/* Private macro -------------------------------------------------------------*/

/* Exported variables --------------------------------------------------------*/

/* Private function prototypes -----------------------------------------------*/
void interpretToEmbeddedMessage(ToEmbedded* toEmbeddedMsg);
void interpretControlCommandMessage(ControlCommand* controlCommandMsg);

/* Exported functions --------------------------------------------------------*/
ProtoStatus APP_PROTO_HANDLE_interpretData(uint8_t* data, size_t data_len)
{
    ToEmbedded* toEmbeddedMsg;
    ProtoStatus status = PROTO_OK;
    if (data_len <= MAX_MESSAGE_LENGTH) {
        if ((toEmbeddedMsg = to_embedded__unpack(NULL, data_len, data)) == NULL) {
            interpretToEmbeddedMessage(toEmbeddedMsg);
        } else {
            status = PROTO_NULL_MSG;
        }
        to_embedded__free_unpacked(toEmbeddedMsg, NULL);
    } else {
        status = PROTO_MSG_TOO_LONG;
    }
    return status;
}

size_t APP_PROTO_HANDLE_bufferFromEmbeddedMsg(FromEmbedded* msg, uint8_t* buffer, size_t max_buffer_len)
{
    size_t packed_length = from_embedded__get_packed_size(msg);
    if (packed_length > max_buffer_len)
        return -1;
    from_embedded__pack(msg, buffer);
    return packed_length;
}

/* Private functions ---------------------------------------------------------*/
void interpretToEmbeddedMessage(ToEmbedded* toEmbeddedMsg)
{
    if (toEmbeddedMsg->contents_case == TO_EMBEDDED__CONTENTS_COMMAND) {
        interpretControlCommandMessage(toEmbeddedMsg->command);
    }
}

void interpretControlCommandMessage(ControlCommand* controlCommandMsg)
{
    switch (controlCommandMsg->commandtype) {
    case CONTROL_COMMAND_TYPE__STOP_LOG:
        APP_CAN_Start();
        break;
    case CONTROL_COMMAND_TYPE__START_LOG:
        APP_CAN_Stop();
        break;
    case CONTROL_COMMAND_TYPE__MARK_LOG:
        /* code */
        break;
    case CONTROL_COMMAND_TYPE__GET_LOGFS_INFO:
        /* code */
        break;
    case CONTROL_COMMAND_TYPE__GET_LOG:
        /* code */
        break;
    case CONTROL_COMMAND_TYPE__DELETE_LOG:
        /* code */
        break;

    default:
        break;
    }
}
